from time import time
from nEngine.Processes import ProcessManager
from nEngine.Events import EventManager

class GameManager:
  """The Game Manager includes functions for managing, unsurprisingly, game
  states. It is a singleton! We ain't managing mo' n' one game, yo!"""
 
  GameManager._currentState = None
  
  @staticmethod
  def setStartState(state):
    """Set the initial state."""
    GameManager._currentState = state
  
  @staticmethod
  def getState():
    return GameManager._currentState
  
  @staticmethod
  def run():
    """Runs, well, the game :)"""
    while GameManager._currentState != None:
      GameManager._currentState.initialise()
      GameManager._currentState.run()
      GameManager._currentState.terminate()
      GameManager._currentState = GameManager._currentState.nextState()

class GameState:
  """This class contains a generic game state. States switch between each other
  on occasion."""
  
  def __init__(self):
    self._nextState = None
  
  
  def initialise(self):
    """Sets GameState in a ready-to-run situation. Reimplement. This is probably
    where you want to set stuff inside the ProcessManager!"""
    print("[ERROR] GameState.initialise() not reimplemented")
  
  def terminate(self):
    """Does final computation on this game state before it is removed."""
    print("[ERROR] GameState.terminate() not reimplemented")
    
  def nextState(self):
    """By default returns no next state."""
    return self._nextState
  
  def run(self):
    """Execute this state's main loop."""
    self.done = False
    
    oldTime = time()
    while not self.done:
      currentTime = time()
      self._pm.run(currentTime - oldTime)
      oldTime = time()
      
  
  def addEntity(self, entity):
    self._entities.append(entity)
    for _, system in self._systems.items():
      if system.check(entity):
        system.addEntity(entity)
  
  def removeEntity(self, entity):
    self._entities.remove(entity)
    for _, system in self._systems.items():
      if system.check(entity):
        system.removeEntity(entity)
  
  def addSystem(self, system):
    self._systems[type(system)] = system
  
  def removeSystem(self, system):
    del self._systems[type(system)]
  
  def tick(self, dt):
    for system in self._systems:
      system.tick(dt)
      
    
    
    
    
    
    
    
    
    
    
    
    