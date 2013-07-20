from nEngine.graphics.HumanView import HumanView
from nEngine.graphics.nGUI import NGUIPane
from nEngine.Input import Input

from sfml import Color

from xml.etree import ElementTree

h = HumanView()
h.WINDOW_WIDTH = 500
h.WINDOW_HEIGHT = 500
h.init("testing...", [])

h.pane = NGUIPane(0, 0, 100, 100, Color.RED)

Input.init(ElementTree.parse('data/keys.xml').getroot(), h)

while True:
  Input.processInput()
  h.clear()
  h.pane.draw(h)
  h.window.display()