from queue import PriorityQueue

from GameModel import Rand
from EntityManager import EntityManager

class World:
  """This class contains the world and all things in it."""
  def __init__(self):
    print("Initialising map")
    self.DEFAULT_W = 40
    self.DEFAULT_H = 30
    
    # Time passed
    self.time = 0
    
    # Queue that manages who needs to be activated next
    self.activationQueue = PriorityQueue()
    
  def generateWorld(self, WORLD_WIDTH = -1, WORLD_HEIGHT = -1):
    print("ERROR: World.GenerateWorld not implemented!")
  
  def createTile(self, tileName, x, y):
    """Creates a new tile object and sets it at the specified location. Please
    always use this function to alter terrain."""
    tile = EntityManager.construct(tileName, self)
    tile.setPosition(x, y)
    self.smap[y][x] = tile
  
  def getTile(self, x, y):
    """Gets tile at a given position, returns None if it's out of bounds."""
    if (x < 0 or x == self.WORLD_WIDTH or
        y < 0 or y == self.WORLD_HEIGHT):
      return None
    return self.smap[y][x]
  

  def addActivationFromNow(self, active):
    """Adds an activation to the activation queue to happen relatively to the
    current time."""
    active.time = active.time + self.time
    self.addActivation(active)
  
  def addActivation(self, active):
    """Adds an activation to the activation queue using active.time as an
    absolute value"""
    self.activationQueue.put(active)
  
  def run(self, dt):
    """Makes the world continue for a wee little while!"""
    if dt <= 0:
      return
    
    # Increment time
    self.time = self.time + dt
    
    # Activate all events until the right moment
    while not self.activationQueue.empty():
    
      # Get top/closest activation
      topActive = self.activationQueue.queue[0]
      
      # Break out of the loop if the activation is in the future
      if topActive.time > self.time:
        break
      
      # Otherwise, remove from queue and activate
      self.activationQueue.get().activate()
  
  def getTiles(self, x, y, w, h):
    """Returns a list with all the tiles starting at x, y and covering the given
    width and height. This is useful for moving large actors/buildings/etc."""
    xs = [x + dx for dx in range(w)]
    ys = [y + dy for dy in range(h)]
    result = []
    for xPos in xs:
      for yPos in ys:
        result.append(self.getTile(xPos, yPos))
    
    return result
  
  def update(self, dt):
    """Meant to update the world according to real-time. Here used for world."""
    self._world.update(dt)
      

  
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
    
  