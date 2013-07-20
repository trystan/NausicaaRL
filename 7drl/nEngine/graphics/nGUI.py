"""Should this be an entity system thing as well?

"""

from sfml import Color, RectangleShape

class NGUIPane:
  def __init__(self, x, y, w, h, backgroundColour = Color.BLACK):
    self._x = x
    self._y = y
    self._w = w
    self._h = h
    self._contents = []
    self._background = RectangleShape()
    self._background.fill_color = backgroundColour
    self._background.position = (self._x, self._y)
    self._background.size = (self._w, self._h)
    
  def draw(self, view):
    view.draw(self._background)
    for content in self._contents:
      content.draw(view)
    

class NGUIFrame:
  def __init__(self, x, y, w, h, title, textOption = "DEFAULT"):
    self._x = x
    self._y = y
    self._w = w
    self._h = h
    self._title = title
  
  def draw(self, view):
    view.drawLine(Color.BLUE, (self._x, self._y), (self.w + self._x, self._y), 2)
    view.drawLine(Color.BLUE, (self._x, self._y), (self._x. self.h +  self._y), 2)