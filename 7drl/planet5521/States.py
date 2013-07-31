from nEngine.Game import GameState
from planet5521.Processes import HumanViewProcess
from nEngine.graphics.ResourceManager import ResourceManager
from nEngine.graphics.nGUI import NGUIImage, NGUIBasicButton
from sfml import Sprite, Color

class MainMenuState(GameState):
  def __init__(self, humanView):
    GameState.__init__(self)
    self._humanView = humanView
    self._humanViewProcess = HumanViewProcess(self._humanView)
  
    
  def initialise(self):
    
    # Background
    self._background = NGUIImage(0,0, Sprite(ResourceManager.getTexture("planet5521/data/screen.png")))
    self._background.name = "background"
    self._humanView.getPane().addChild(self._background)
    
    # Buttons
    self._startButton = NGUIBasicButton(500, 350, 200, 75, "Start")
    self._exitButton = NGUIBasicButton(500, 450, 200, 75, "Exit")
    
    self._startButton.style = self._exitButton.style =  "default_title"
    self._startButton.styleFocus = self._exitButton.styleFocus = "default_title_focus"
    self._startButton.stylePrimed = self._exitButton.stylePrimed = "default_title_primed"
    self._startButton.backgroundColour = self._exitButton.backgroundColour = Color(80, 25, 25, 100)
    self._startButton.backgroundColourFocus = self._exitButton.backgroundColourFocus = Color(80, 25, 25, 200)
    self._startButton.backgroundColourPrimed = self._exitButton.backgroundColourPrimed = Color(80, 25, 25, 255)
    
    self._humanView.getPane().addChild(self._startButton)
    self._humanView.getPane().addChild(self._exitButton)
    
    # Make humanview visible
    self._pm.processList.append(HumanViewProcess(self._humanView)) 
  
  def terminate(self):
    """Does final computation on this game state before it is removed."""
    self._humanView.getPane().clear()
    
  def nextState(self):
    """By default returns no next state."""
    return self._nextState