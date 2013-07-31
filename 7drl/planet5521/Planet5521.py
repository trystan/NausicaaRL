from nEngine.Game import GameManager
from nEngine.graphics.TextManager import TextManager
from nEngine.graphics.HumanView import HumanView

from planet5521.States import MainMenuState

class Planet5521(GameManager):
  """This class contains the game itself."""
  def __init__(self):
    GameManager.__init__(self)
    
    self.humanView = HumanView()
    self.humanView.init("Planet 5521", "planet5521/data/graphics.xml")
    TextManager.loadFromFile("planet5521/data/fonts.xml")
    
    self._currentState = MainMenuState(self.humanView)

