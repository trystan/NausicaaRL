from nEngine.Game import GameState
from nEngine.graphics.ResourceManager import ResourceManager
from nEngine.Processes import ProcessManager
from nEngine.graphics.nGUI import NGUIImage
from sfml import Sprite

class MainMenuState(GameState):
  def __init__(self):
    self._nextState = None
    self._pm = ProcessManager()
  
  def setHumanView(self, humanView):
    self._humanView = humanView
    
  def initialise(self):
    self._background = NGUIImage(0,0, Sprite(ResourceManager.getTexture("planet5521/data/screen.png")))
    self._humanView.getPane().addChild(self._background)
  
  def terminate(self):
    """Does final computation on this game state before it is removed."""
    print("[ERROR] GameState.terminate() not reimplemented")
    
  def nextState(self):
    """By default returns no next state."""
    return self._nextState
  
  def run(self):
    """Execute this state's main loop."""
    self.done = False