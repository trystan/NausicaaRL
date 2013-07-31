from time import time
from nEngine.Processes import ProcessManager
from nEngine.Events import EventManager

class GameManager:
  """The Game Manager includes functions for managing, unsurprisingly, game
  states. It is a singleton! We ain't managing mo' n' one game, yo!"""
 
  def __init__(self):
    self._currentState = None
  
  def setStartState(self, state):
    """Set the initial state."""
    GameManager._currentState = state
  
  def getState(self):
    return GameManager._currentState
  
  def run(self):
    """Runs, well, the game :)"""
    while self._currentState != None:
      self._currentState.initialise()
      self._currentState.run()
      self._currentState.terminate()
      self._currentState = self._currentState.nextState()




class GameState:
  """This class contains a generic game state. States switch between each other
  on occasion."""
  
  def __init__(self):
    self._nextState = None
    self._pm = ProcessManager()
  
  
  def initialise(self):
    """Sets GameState in a ready-to-run situation. Reimplement. This is probably
    where you want to set stuff inside the ProcessManager!"""
    pass
  
  def terminate(self):
    """Does final computation on this game state before it is removed."""
    pass
    
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
      
      
    
    
    
    
    
    
    
    
    
    
    
    