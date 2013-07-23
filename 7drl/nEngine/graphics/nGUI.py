#TODO : what happens if you move from another Base into a new Base? You'll get
# a mouseEnterEvent in the new one, but not in the old one... 

from sfml import Color, RectangleShape
from nEngine.Options import Options

class NGUIBase:
  """A basic area that can receive mouse/keyboard inputs."""
  def __init__(self, x, y, w, h):
    # THe name can be used for debugging purposes.
    self.name = "Theodore"
    # There will be a hierarchy. Everyone has a parent, except the root.
    self._parent = None
    self._x = x
    self._y = y
    self._w = w
    self._h = h
    
    # Absolute x and y positions. These are calculated based on the parent!
    self._ax = x
    self._ay = y

    # This can be either self, None, or perhaps a child in the NGUIPane case
    self._mouseOverFocus = None
    
    self._listeners = []
    self.addListener(self)
  
  def setParent(self, parent):
    """Set parent and update absolute position."""
    self.parent = parent
    self._ax = parent._ax + self._x
    self._ay = parent._ay + self._y
  
  def addListener(self, listener):
    self._listeners.append(listener)
    
  def _onKeyboardEvent(self, event):
    """Keyboard events are not consumed by default?"""
    return False
  
  def _checkMousePosition(self, position):
    """Checks whether the mouse is within the bounds."""
    (mx, my) = position
    if mx < self._ax or my < self._ay:
      return False
    if mx > self._ax + self._w or my > self._ay + self._h:
      return False
    return True
  
  def _onMouseWheelEvent(self, event):
    # If the mouse wasn't within these bounds, it is not consumed.
    if not self._checkMousePosition(event.position):
      return False
    
    for listener in self._listeners:
      listener.onMouseWheelEvent(event)
    # Consumed!
    return True
  
  def _onMouseButtonEvent(self, event):
    # If the mouse wasn't within these bounds, it is not consumed.
    if not self._checkMousePosition(event.position):
      return False
    
    for listener in self._listeners:
      listener.onMouseButtonEvent(event)
    # Consumed!
    return True
  
  def _onMouseMoveEvent(self, event):
    if not self._checkMousePosition(event.position):
      # If mouse is no longer within bounds
      if self._checkMousePosition(event.oldPosition):
        # But was within bounds previously, then there's a mouseExitEvent
        for listener in self._listeners:
          listener.onMouseExitEvent(event)
      # Since the mouse is no longer within this Base's bounds, don't consume it
      return False
    
    # Mouse is within bounds
    if not self._checkMousePosition(event.oldPosition):
      # And if it wasn't previously, mouseEnterEvent
      for listener in self._listeners:
        listener.onMouseEnterEvent(event)
    
    # Whether it was or wasn't within before, there's a mouseMouseEvent
    for listener in self._listeners:
      listener.onMouseMoveEvent(event)
    # Consumed!
    return True

  # MOUSE FOCUS
  
  def _setMouseFocus(self):
    self._mouseOverFocus = self
    if self._parent != None:
      self._parent._updateMouseFocus(self)
  
  # TODO this needs thinking
  def _updateMouseFocus(self, child):
    if self._mouseOverFocus == child: # If the child kept the focus, do nothing
      return
    # If there was no focus ever, update all parents
    elif self._mouseOverFocus == None:
      self._mouseOverFocus = child
      self._parent._updateMouseFocus(self)
    # If there was a different child
    else:
      
      
  # EVENT CALLBACKS
  
  def onKeyboardEvent(self, event):
    pass
  
  def onMouseWheelEvent(self, event):
    if Options.DEBUG:
      print("["+self.name+"] onMouseWheelEvent")
      print(str(event.delta) + ", " + str(event.position))
  
  def onMouseButtonEvent(self, event):
    if Options.DEBUG:
      print("["+self.name+"] onMouseButtonEvent")
      print(str(event.pressed) + ", " + str(event.button) + ", " + str(event.position))
  
  def onMouseEnterEvent(self, event):
    self._setMouseFocus()
    if Options.DEBUG:
      print("["+self.name+"] onMouseEnterEvent")
      print(str(event.oldPosition) + " -> " + str(event.position))
    pass
  
  def onMouseExitEvent(self, event):
    if Options.DEBUG:
      print("["+self.name+"] onMouseExitEvent")
      print(str(event.oldPosition) + " -> " + str(event.position))
    pass
  
  def onMouseMoveEvent(self, event):
    if Options.DEBUG:
      #print("["+self.name+"] onMouseMoveEvent")
      #print(str(event.oldPosition) + " -> " + str(event.position))
      pass


class NGUIPane(NGUIBase):
  """Basic content pane"""
  def __init__(self, x, y, w, h, backgroundColour = None):
    NGUIBase.__init__(self, x, y, w, h)
    self._children = []
    if backgroundColour == None:
      self._background = None
    else:
      self._background = RectangleShape()
      self._background.fill_color = backgroundColour
      self._background.position = (self._ax, self._ay)
      self._background.size = (self._w, self._h)
  
  # Events: these must be passed on to its contents. They only apply here
  # if they were not consumed by the children. THE CHILDREEEEN!
  
  def _onKeyboardEvent(self, event):
    for child in reversed(self._children):
      if child._onKeyboardEvent(event):
        return True
    return False
  
  def _onMouseWheelEvent(self, event):
    for child in reversed(self._children):
      if child._onMouseWheelEvent(event):
        return True
    
    return NGUIBase._onMouseWheelEvent(self, event)
  
  def _onMouseButtonEvent(self, event):
    for child in reversed(self._children):
      if child._onMouseButtonEvent(event):
        return True
    
    return NGUIBase._onMouseButtonEvent(self, event)
  
  def _onMouseMoveEvent(self, event):
    for child in reversed(self._children):
      if child._onMouseMoveEvent(event):
        return True
    
    return NGUIBase._onMouseMoveEvent(self, event)
  
  
  # HIERARCHY
  
  def setParent(self, parent):
    NGUIBase.setParent(self, parent)
    self._background.position = (self._ax, self._ay)
  
  def addChild(self, child):
    child.setParent(self)
    self._children.append(child)
  
  
  # DRAWING
  
  def draw(self, view):
    if self._background != None:
      view.drawSprite(self._background)
    for child in self._children:
      child.draw(view)
    

class NGUIFrame(NGUIPane):
  def __init__(self, x, y, w, h, backgroundColour = Color.BLACK, frameColour = Color.WHITE, thickness=1, title = None, style = "default"):
    NGUIPane.__init__(self, x, y, w, h, backgroundColour)
    self._title = title
    self._frameColour = frameColour
    self._thickness = thickness
    self._title = title
    self._style = style
  
  def draw(self, view):
    NGUIPane.draw(self, view)
    view.drawLine(self._frameColour, (self._ax, self._ay), (self._w + self._ax, self._ay), self._thickness)
    view.drawLine(self._frameColour, (self._ax, self._ay), (self._ax, self._h + self._ay), self._thickness)
    view.drawLine(self._frameColour, (self._w + self._ax, self._ay), (self._w + self._ax, self._ay + self._h), self._thickness)
    view.drawLine(self._frameColour, (self._ax, self._h + self._ay), (self._ax + self._w, self._ay + self._h), self._thickness)
    
    
    
    
    
    