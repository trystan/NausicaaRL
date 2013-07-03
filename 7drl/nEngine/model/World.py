from queue import PriorityQueue

from nEngine.EntityManager import EntityManager

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
      
  