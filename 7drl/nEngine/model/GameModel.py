from collections import deque

from nEngine.Activation import Activation

"""This module contains all the classes which compose the entities in the game."""

class Part:
  """This class represents a body part of an actor."""
  
  def __init__(self, blueprint, actor):
    self.bp = blueprint
    self.equipped = None
    self._actor = actor
    self.hp = self.bp.hp
  
  def canEquip(self, item):
    """Returns whether the given item can be equipped in the current part."""
    # Simply checks whether the id of this part is in the equippable ids
    return self.bp.id in item.bp.equipAt
  
  def equip(self, item):
    """Equips the item in this bodypart."""
    if not self.canEquip(item):
      print("[WARNING] Trying to equip unequippable item.")
      return
    
    self.unequip()
    self.equipped = item
    
  def unequip(self):
    """Removes the currently equipped item"""
    self.equipped = None

    
    
class Entity:
  """ All "things" within the game are Entities (e.g. tiles, objects, creatures,
  etc), and the main functionality is that all Entities work as containers.
  In other words, all entities "carry" or "hold" things. These things might,
  or might not be visible:
  They are stored in dictionary "contents", mapping other Entities to a boolean
  stating whether they are visible or not. """
  def __init__(self, blueprint, world):
    self.bp = blueprint
    self.display = self.bp.display.construct()
    self._world = world
      
    # Container / parent hierarchy
    self.contents = {}
    self.parent = None
  
  def canPass(self):
    return self.bp.passable
  
  def setAllVisible(self, visible):
    for entity in self.contents.keys():
      self.contents.update(entity=visible)
  
  def setVisible(self, entity, visible):
    self.contents.update(entity=visible)

  def getVisibleItems(self):
    """This method returns a list of all visible objects of a tile. """
    result = []
    visibleObjects = deque([self])
    while len(visibleObjects) > 0:
      entity = visibleObjects.popleft() 
      result.append(entity)
      for (child, visible) in entity.contents.items():
        if visible:
          visibleObjects.append(child) 
    return result
  
  def getOpenableItems(self):
    """This method returns a list of all closed, openable and visible objects."""
    return [item for item in self.getVisibleItems() if item.bp.openable and not item.isOpen]
  
  def getClosableItems(self):
    """This method returns a list of all closed, openable and visible objects."""
    return [item for item in self.getVisibleItems() if item.bp.openable and item.isOpen]

  def addContent(self, entity, visible=True):
    """This method allows moving a content from an entity to this entity."""
    # If this object was elsewhere, remove it from there.
    if(entity.parent != None):
      entity.parent.removeContent(entity)
      
    # Then add it locally
    self.contents[entity] = visible
    entity.parent = self
  
  def removeContent(self, entity):
    """Removes content from this entity. Entity.parent becomes None!"""
    entity.parent = None
    del self.contents[entity]
    
  def getPickableItems(self):
    """This method iterates the list of all visible items of an entity
    and returns those which are pickable."""
    visibleItemsList = self.getVisibleItems()[1:]
    pickableItems = []
    for item in visibleItemsList:
      if (item.bp.pickup):
        pickableItems.append(item)
    return pickableItems 
    
  def getMainTile(self):
    """Returns the root (tile) of the contents/parent relation."""
    root = self
    while root.parent != None:
      root = root.parent
      
    return root
  
  def isVisible(self):
    """Checks whether this entity is visible in its parent (!!!). If it's a tile,
    it's visible."""
    
    if self.parent == None:
      return True
    
    return self.parent.contents[self]
        
  def die(self):
    """Method that removes the entity from the game."""
    if self.parent != None:
      del self.parent.contents[self]
  
  def getDescription(self):
    """Gets the blueprint's description. Specific classes should add more stuff."""
    desc = self.bp.description
    if self.bp.passable:
      desc += " You can pass through this."
    else:
      desc += " You cannot pass through this."
    return desc
  
  def getEntity(self, name):
    """Returns a content entity of the type given by name."""
    for entity in self.contents.keys():
      if entity.bp.name == name:
        return entity
  
  def isMainTile(self, tile):
    """Checks whether the given tile is this object's principal tile."""
    return tile == self.getMainTile()

  def update(self, dt):
    """Meant to update the world according to real-time."""
    self.display.update(dt)
    for child in self.contents:
      child.update(dt)
    
    
    
class Tile(Entity):
  """ A Tile represents a space on the game board. It can be passable or not!"""
  def __init__(self, blueprint, world):
    Entity.__init__(self, blueprint, world)
    self.x = -1
    self.y = -1
  
  def setPosition(self, x, y):
    self.x = x
    self.y = y
  
  def canPass(self):
    """A tile is passable if it is a passable entity and none of its contents
    are impassable."""
    if not self.bp.passable:
      return False
    for a in self.contents.keys():
      if(not a.canPass()):
        return False
    return True

    
  # For tiles, width and height of items matters. When removing or adding, it is
  # necessary to also check other tiles affected by the width/height of the object
  def addContent(self, entity, visible=True):
    """This method allows moving a content from an entity to this entity."""
    parentTiles = self._world.getTiles(self.x, self.y,
                                       entity.bp.w, entity.bp.h)

    for tile in parentTiles:
      tile.contents[entity] = visible
    
    if(entity.parent != None):
      del entity.parent.contents[entity]
    
    entity.parent = self
  
  def removeContent(self, entity):
    """Removes content from this entity. Entity.parent becomes None!"""
    parentTiles = self._world.getTiles(self.x, self.y,
                                       entity.bp.w, entity.bp.h)
    
    for tile in parentTiles:
      del tile.contents[entity]
    entity.parent = None
  
  
  
  
class Object(Entity):
  """An object has a physical presence within the game _world. It should be
  of a certain typed defined in XML."""
  
  def __init__(self, blueprint, world):
    Entity.__init__(self, blueprint, world)

  def getPos(self):
    """Returns the tile where this object is at."""
    tile = self.getMainTile()
    return (tile.x, tile.y)

  def getDescription(self):
    """Adds pickup line property."""
    desc = Entity.getDescription(self)
    if self.bp.pickup:
      desc += " You can pick this up."
    else:
      desc += " You can't pick this up."
    return desc
  
  def isWeapon(self):
    """Checks for non-trivial values in one of the weapon related attributes."""
    return self.attackSpeed > 0
  
  def isArmour(self):
    """Checks for non-trivial values in one of the armour related attributes."""
    return self.protection > 0
    
    
class Crop(Object):
  """Represents a crop that is being grown."""
  
  def __init__(self, blueprint, world):
    Object.__init__(self, blueprint, world)
    self.cropState = 0
    self.care = self.bp.care
    self.setupActivations()
    self._animationOrder = ["SEEDS", "MIDWAY", "GROWN"]
    self.setDisplay()
    
  
  def setupActivations(self):
    """Sets up initial activations for growing the crop and it losing care."""
    self._world.addActivationFromNow(Activation(self.bp.growth[self.cropState], self.growCrop))
    self._world.addActivationFromNow(Activation(self.bp.careLossInterval, self.loseCare))
  
  
  def growCrop(self):
    """Grows the crop to the next level!!!11one"""
    self.cropState = self.cropState + 1
    if self.cropState > len(self.bp.growth)-1:
      self.die()
      return
    
    self.setDisplay()
    
    # Create an activation that calls grow crop again in the future.
    self._world.addActivationFromNow(Activation(self.bp.growth[self.cropState], self.growCrop))
  
  def loseCare(self):
    """Crop care goes down over time"""
    self.care = self.care - 1
    
    self._world.addActivationFromNow(Activation(self.bp.careLossInterval, self.loseCare))
  
  def setDisplay(self):
    """Set display: this really shouldn't be here though. These guys shouldn't
    know about displays"""
    self.display.startAnimation(self._animationOrder[self.cropState])
  
  def die(self):
    Object.die(self)
    #self.game.addMessage("A cereal crop withers.")  

    
    
  
class Container(Object):
  """ Containers are objects that contain something. They may be openable
  or not. A container is assumed openable by default. 
  Examples of openable objects: chests, cabinets, etc. """
  
  def __init__(self, blueprint, world):
    Object.__init__(self, blueprint, world)
    self.isOpen = self.bp.isOpen
  
  def open(self, actor = None):
    """This method makes a container opened. """
    self.isOpen = True
    self.setAllVisible(self, True)
    self.display.startAnimation("OPEN")
  
  def close(self, actor = None):
    """This method makes a container closed. """  
    self.isOpen = False 
    self.setAllVisible(self, False)
    self.display.startAnimation("CLOSED")
    
    
    
    
  
class Door(Object):
  """ Containers are objects that contain something. They may be openable
  or not. A container is assumed openable by default. 
  Examples of openable objects: chests, cabinets, etc. """
  
  def __init__(self, blueprint, world):
    Object.__init__(self, blueprint, world)
    self.isOpen = self.bp.isOpen
  
  def open(self, actor = None):
    """This method makes a container opened. """
    self.isOpen = True
    self.display.startAnimation("OPEN")
  
  def close(self, actor = None):
    """This method makes a container closed. """  
    self.isOpen = False
    self.display.startAnimation("CLOSED")
  
  def canPass(self):
    """Doors are passable if they are open!"""
    return self.isOpen


    
    
class Actor(Object):
  """ Actors are any objects that may move around in the _world, perform actions,
  and generally have an active presence in the _world. """

  def __init__(self, blueprint, world):
    Object.__init__(self, blueprint, world)
    # Set equipment status. Indexed by partIndex, value is item!
    self._parts = [bp.construct(self) for bp in self.bp.parts]

  def step(self, dx, dy):
    """This makes the actor move, hopefully just by 1! Returns how long he's
    going to have to wait."""
    if(abs(dx) > 1 or abs(dy) > 1):
      print("[ERROR] Actor trying to move by " + dx + ", " + dy + ".")
      return -1
    
    # See whether the destination tile is inside the map bounds
    pos = self.getPos()
    destTile = self._world.getTile(pos[0] + dx, pos[1] + dy)
    if destTile == None:
      #self.game.addMessage("*bump*")
      return -1
    
    # If the destination tile is not passable, the actor bumps into it
    if not destTile.canPass():
      return -1
    
    # Move the actor
    destTile.addContent(self, self.isVisible())
    
    # If it's a diagonal, it takes longer (roughly sqrt(200), 200 = 10^2 + 10^2
    if abs(dx) + abs(dy) > 1:
      return 14
    return 10
    
  def pickup(self, items):
    """The actor picks up the items. No checks are made as to the origin of the
    items - checks must be made prior!""" 
    for item in items:
      self.addContent(item, False)
    
    return 3*len(items)
  
  def drop(self, items):
    """Drops stuff he is carrying. No checks are made as to the origin of these
    items - checks must be made prior.
    Returns time it took to do this. TODO ALL THESE FUNCTIONS SHOULD RETURN THIS TIME."""   
    for item in items:
      # Checks whether the item was equipped, and unequips it.
      equippedAt = self.isEquipped(item)
      if equippedAt != None:
        self.unequip(equippedAt)
      self.parent.addContent(item, True)
      
    return 2*len(items)
  
  def open(self, entity):
    entity.open(self)
  
  def close(self, entity):
    entity.close(self)
  
  def unequip(self, part):
    """Removes whatever is in part."""
    return part.unequip()
  
  def equip(self, part, item):
    """Equip given item in given part. Returns whatever was there last."""
    if not part in self._parts:
      print("[ERROR] Equipping in part that does not belong to actor.")
      return
    
    # Check whether the item is equipped elsewhere, and unequip it from there.
    equippedAt = self.isEquipped(item)
    if equippedAt != None:
      self.unequip(equippedAt)
      
    # If the part currently selected has another item there, unequip it too
    if part.equipped != None:
      self.unequip(part)
    
    # Finally, unequip all the things
    part.equip(item)
    
  def isEquipped(self, item):
    """Checks whether the given item is equipped. If it is, returns the part in
    which it is equipped, otherwise returns None."""
    for part in self._parts:
      if part.equipped == item:
        return part
    return None
    
    
    
class Hero(Actor):
  """ The player's class! """

  def __init__(self, blueprint, world):
    Actor.__init__(self, blueprint, world)
  
  def step(self, dx, dy):
    """Steps normally, but also writes a message in case there's anything he can
    see in his new position."""
    # Move first
    moved = Actor.step(self, dx, dy)
    
    # If we didn't move, do nothing
    if moved < 0:
      return moved
    
    # If there aren't any visible items, end
    visibleItems = self.parent.getVisibleItems()
    visibleItems = [item for item in visibleItems if (item != self and item != self.parent)]
    if len(visibleItems) == 0:
      return moved
    
    ## If there are visible items, write them out in message history.
    #text = "Here you see " + Utility.entitiesToText(visibleItems) + "."
    #self.game.addMessage(text)
    
    return moved
  
  
  
  
  
  