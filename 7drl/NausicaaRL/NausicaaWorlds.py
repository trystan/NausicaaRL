from nEngine.model.World import World
from nEngine.Rand import Rand
from nEngine.EntityManager import EntityManager

class Village(World):
  """Represents the hero's village!"""
  

  def generateWorld(self, WORLD_WIDTH = -1, WORLD_HEIGHT = -1):
    if WORLD_WIDTH == -1:
      WORLD_WIDTH = self.DEFAULT_W
    if WORLD_HEIGHT == -1:
      WORLD_HEIGHT = self.DEFAULT_H
    self.WORLD_WIDTH = WORLD_WIDTH
    self.WORLD_HEIGHT = WORLD_HEIGHT
    
    self.CROP_WIDTH = 10
    self.CROP_HEIGHT = 5
    
    self.initMap()
    print("Generating map")
    self.generateMap()
    print("Placing hero")
    self.placeActor()
    print("Placing crops")
    self.placeCropZone()
    print("Placing rocks")
    self.placeRocks()
    print("Placing pebbles")
    self.placePebbles()
    print("Placing windmill")
    self.placeWindmill()
    print("Placing equipment")
    self.placeEquipment()
    
  def initMap(self):
    """Creates walls in the entire map."""
    self.smap = []
    for _ in range(self.WORLD_HEIGHT):
      l = []
      for _ in range(self.WORLD_WIDTH):
        l.append(None)
      self.smap.append(l)
  
  def generateMap(self):
    """Creates the village map."""
    
    # First initialise everything to grass.
    for i in range(self.WORLD_WIDTH):
      for j in range(self.WORLD_HEIGHT):
        self.createTile("grass", i, j)
  
  def placeCropZone(self):
    # Creates the crop zone.
    self.generateCropZone(self.CROP_WIDTH, self.CROP_HEIGHT,
                          Rand.r.randint(0, self.WORLD_WIDTH-self.CROP_WIDTH-2),
                          Rand.r.randint(0, self.WORLD_HEIGHT-self.CROP_HEIGHT-2))
  
  def generateCropZone(self, w, h, x, y):
    """Creates a crop growing zone with the given size at the given location.
    Returns whether it succeeded or not."""
     
    for i in [posX + x for posX in range(w+2)]:
      for j in [posy + y for posy in range(h+2)]:
        if not self.getTile(i, j).canPass():
          return False
    
    # All terrain is passable!
    
    for i in [posX + x + 1 for posX in range(w)]:
      for j in [posy + y + 1 for posy in range(h)]:
        crop = EntityManager.construct("cereal", self)
        self.getTile(i, j).addContent(crop, True)
    
    # Create fences
    xts = [(posX + x, y) for posX in range(w+2)]
    xbs = [(posX + x, y+h+1) for posX in range(w+2)]
    yls = [(x, posY + y + 1) for posY in range(h)]
    yrs = [(x+w+1, posY + y + 1) for posY in range(h)]
    toFence = [xts, xbs, yls, yrs]
    for row in toFence:
      for (fx, fy) in row:
        self.getTile(fx, fy).addContent(EntityManager.construct("fence", self))
    
    # To choose gate positions, remove corners.
    xts = xts[1:-1]
    xbs = xbs[1:-1]
    forGate = []
    forGate.extend(xts)
    forGate.extend(xbs)
    forGate.extend(yls)
    forGate.extend(yrs)
    (gateX, gateY) = forGate[Rand.r.randint(0, len(forGate)-1)]
    tile = self.getTile(gateX, gateY)
    tile.removeContent(tile.getEntity("fence"))
    tile.addContent(EntityManager.construct("fence gate", self))
    

  def placeActor(self):
    """Finds a passable place to put the character at."""
    while(True):
      x = Rand.r.randint(0, self.WORLD_WIDTH -1)
      y = Rand.r.randint(0, self.WORLD_HEIGHT -1)
      tile = self.getTile(x, y)
      if(tile.canPass()):
        break
    
    actor = EntityManager.construct("nausicaa", self)
    actor.parent = tile
    tile.contents[actor] = True
    self.hero = actor
    
  def placeEquipment(self):
    """Drops some equipment where the actor is."""
    tile = self.hero.parent
    tile.addContent(EntityManager.construct("leggings", self))
    tile.addContent(EntityManager.construct("ceramic sword", self))
    tile.addContent(EntityManager.construct("ceramic mace", self))
    tile.addContent(EntityManager.construct("flight cap", self))
  
  def placeRocks(self):
    for _ in range(5):
      while(True):
        x = Rand.r.randint(0, self.WORLD_WIDTH -1)
        y = Rand.r.randint(0, self.WORLD_HEIGHT -1)
        tile = self.getTile(x, y)
        if(tile.canPass()):
          break
    
      rock = EntityManager.construct("rock", self)
      rock.parent = tile
      tile.contents[rock] = True
    
  def placePebbles(self):
    for _ in range(15):
      while(True):
        x = Rand.r.randint(0, self.WORLD_WIDTH -1)
        y = Rand.r.randint(0, self.WORLD_HEIGHT -1)
        tile = self.getTile(x, y)
        if(tile.canPass()):
          break
    
      rock = EntityManager.construct("pebble", self)
      rock.parent = tile
      tile.contents[rock] = True
      rock = EntityManager.construct("pebble", self)
      rock.parent = tile
      tile.contents[rock] = True
      
  def placeWindmill(self):
    for _ in range(10):
      while(True):
        x = Rand.r.randint(0, self.WORLD_WIDTH -2)
        y = Rand.r.randint(0, self.WORLD_HEIGHT -2)
        tile1 = self.getTile(x, y)
        tile2 = self.getTile(x+1, y)
        tile3 = self.getTile(x, y+1)
        tile4 = self.getTile(x+1, y+1)
        if(tile1.canPass() and tile2.canPass() and tile3.canPass() and tile4.canPass()):
          break
    
      rock = EntityManager.construct("windmill", self)
      tile1.addContent(rock)
      #break
    