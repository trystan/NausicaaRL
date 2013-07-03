
import xml.etree.ElementTree as ElementTree

from nEngine.GameState import GameManager
from nEngine.graphics.Display import Display
from nEngine.Input import Input
from nEngine.graphics.nGUI.nGUI import InitGUI
from nEngine.EntityManager import EntityManager
from NausicaaRL.NausicaaStates import TitleScreenState


class NausicaaRL(GameManager):
  """This class contains the game itself."""
  def __init__(self):
    GameManager.__init__(self)
    
    tree = ElementTree.parse("data/config.xml")
    root = tree.getroot()
    
    Display.init(root.find("display"))
    Input.init(root.find("keyconfig"))
    
    InitGUI()
    
    # Read XML
    EntityManager.parseFile("data/entities.xml")
    
    self._currentState = TitleScreenState()




    