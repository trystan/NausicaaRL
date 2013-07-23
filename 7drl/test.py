from nEngine.graphics.HumanView import HumanView
from nEngine.graphics.nGUI import NGUIFrame
from nEngine.Input import Input

from sfml import Color

from xml.etree import ElementTree

h = HumanView()
h.WINDOW_WIDTH = 800
h.WINDOW_HEIGHT = 500
h.init("testing...", [])

frame1 = NGUIFrame(50, 150, 300, 200, Color.RED, Color.WHITE)
frame1.name = "name1"
frame2 = NGUIFrame(75, 200, 300, 200, Color.BLUE, Color.WHITE)
frame2.name = "name2"
subframe = NGUIFrame(10, 10, 40, 20, Color.GREEN, Color.WHITE)
subframe.name = "subframe"

frame2.addChild(subframe)
h._pane.addChild(frame1)
h._pane.addChild(frame2)

Input.init(ElementTree.parse('data/keys.xml').getroot(), h)

while True:
  Input.processInput()
  h.draw()