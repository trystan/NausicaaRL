from EntityManager import *
from World import *
from View import *
from Input import *
from nGUI import *
from GameState import *
from NausicaaStates import *

class NausicaaRL(GameManager):
  """This class contains the game itself."""
  def __init__(self):
    GameManager.__init__(self)
    
    tree = ElementTree.parse("config.xml")
    root = tree.getroot()
    
    View.init(root.find("display"))
    Input.init(root.find("keyconfig"))
    
    InitGUI()
    
    # Read XML
    EntityManager.parseFile("entities.xml")
    
    self._currentState = TitleScreenState()


if __name__ == "__main__":
    game = NausicaaRL()
    game.run()

    