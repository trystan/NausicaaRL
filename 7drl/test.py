from nEngine.graphics.HumanView import HumanView
from nEngine.graphics.nGUI import NGUIFrame, NGUIBasicButton
from nEngine.Input import Input

from sfml import Color

from xml.etree import ElementTree

class PriorityListener:
  def __init__(self, base):
    self.base = base
  
  def onMouseDownEvent(self, event):
    if self.base._mouseFocus:
      parent = self.base._parent
      if parent != None:
        parent.removeChild(self.base)
        parent.addChild(self.base)

h = HumanView()
h.WINDOW_WIDTH = 800
h.WINDOW_HEIGHT = 500
h.init("testing...", [])

frame1 = NGUIFrame(50, 150, 300, 200, Color.CYAN, Color.WHITE)
frame1.name = "name1"
frame2 = NGUIFrame(75, 200, 300, 200, Color.BLUE, Color.WHITE)
frame2.name = "name2"
subframe = NGUIFrame(10, 10, 40, 20, Color.GREEN, Color.WHITE)
subframe.name = "subframe"
button = NGUIBasicButton(10, 10, 500, 250, "OK")
button.name = "Button"

frame2.addChild(subframe)
h._pane.addChild(frame1)
h._pane.addChild(frame2)
frame1.addChild(button)

frame1.addListener(PriorityListener(frame1))
frame2.addListener(PriorityListener(frame2))
button.addListener(PriorityListener(button))

Input.init(ElementTree.parse('NausicaaRL/data/keys.xml').getroot(), h)

while True:
  Input.processInput()
  h.draw()