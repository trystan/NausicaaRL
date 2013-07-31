#TODO : Deal with event.consumed and whether listeners return false...

from sfml import Color, RectangleShape
from nEngine.Options import Options
from nEngine.graphics.TextManager import TextManager


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

    # Sprites
    self._sprites = []
    
    # Input
    self._mouseFocus = False  # Is the mouse right on top of this
    self._mouseWithin = False # Is the mouse within the area
    
    self._listeners = []
    if Options.DEBUG:
      self.addListener(DebugEventListener(self))
  
  def setParent(self, parent):
    """Set parent and update absolute position."""
    self._parent = parent
    if parent != None: # TODO This should go to a recalculate function that can be called from more places.
      self._ax = parent._ax + self._x
      self._ay = parent._ay + self._y
  
  def getRoot(self):
    if self._parent == None:
      return self
    return self._parent.getRoot()
  
  def addListener(self, listener):
    print(listener)
    self._listeners.append(listener)
    print(self._listeners)
    
  def _onKeyboardEvent(self, event):
    """Keyboard events are not consumed by default?"""
    return False
  
  def mouseFocus(self):
    """To check whether this NGUIBase has mouse focus."""
    return self._mouseFocus
  
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
    if not self._mouseFocus:
      return False
    
    for listener in self._listeners:
      try:
        listener.onMouseWheelEvent(event)
      except AttributeError:
        pass
    # Consumed!
    return True
  
  def _onMouseButtonEvent(self, event):
    # If the mouse wasn't within these bounds, it is not consumed.
    if not self._mouseFocus:
      return False
    
    for listener in self._listeners:
      try:
        if event.pressed:
          listener.onMouseDownEvent(event)
        else:
          listener.onMouseUpEvent(event)
      except AttributeError:
        pass
    # Consumed!
    return True
  
  def _onMouseMoveEvent(self, event):
    if not self._checkMousePosition(event.position):
      if self._checkMousePosition(event.oldPosition):
        self._onMouseExitEvent(event)
      return False
    
    # Mouse is within bounds
    if not self._checkMousePosition(event.oldPosition):
      # And if it wasn't previously, mouseEnterEvent
      self._onMouseEnterEvent(event)
    
    # Whether it was or wasn't within before, there's a mouseMouseEvent
    for listener in self._listeners:
      try:
        listener.onMouseMoveEvent(event)
      except AttributeError:
        pass
    # Consumed!
    return False
  

  def _onMouseEnterEvent(self, event):
    self._mouseWithin = True
    for listener in self._listeners:
      try:
        listener.onMouseEnterEvent(event)
      except AttributeError:
        pass
  
  def _onMouseExitEvent(self, event):
    self._mouseWithin = False
    #self._removeMouseFocus()
    for listener in self._listeners:
      try:
        listener.onMouseExitEvent(event)
      except AttributeError:
        pass
    
  # MOUSE FOCUS
  
  def _getMouseFocus(self, position):
    """Gets whichever GUIBase has mouseFocus """
    if self._checkMousePosition(position):
      return self
    else:
      return None
    
  def _onMouseFocusEvent(self, event):
    self._mouseFocus = True
    for listener in self._listeners:
      try:
        listener.onMouseFocusEvent(event)
      except AttributeError:
        pass
  
  def _onMouseDefocusEvent(self, event):
    self._mouseFocus = False
    for listener in self._listeners:
      try:
        listener.onMouseDefocusEvent(event)
      except AttributeError:
        pass
    
  # EVENT CALLBACKS

  def draw(self, view):
    if Options.DEBUG:
      if self._mouseWithin == True:
        r = RectangleShape()
        r.outline_color = Color.RED
        r.outline_thickness = 3
        r.fill_color = Color.TRANSPARENT
        r.position = (self._ax, self._ay)
        r.size = (self._w, self._h)
        view.drawSprite(r)
      if self._mouseFocus:
        view.drawLine(Color.RED, (self._ax, self._ay),
                                 (self._ax + self._w, self._ay + self._h))
        view.drawLine(Color.RED, (self._ax + self._w, self._ay),
                                 (self._ax, self._ay + self._h))


  def __str__(self):
    return self.name




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
  
  
  def _checkMouseOnChild(self, position):
    """Checks that the mouse is within this frame, but inside some child."""
    for child in self._children:
      if child._checkMousePosition(position):
        return True
    
    return False
  
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
  
  # MOUSE FOCUS
  
  def _getMouseFocus(self, position):
    """Gets whichever GUIBase has mouseFocus """
    mouseFocus = None
    for child in self._children:
      newFocus = child._getMouseFocus(position)
      if newFocus != None:
        mouseFocus = newFocus
      
    if mouseFocus != None:
      return mouseFocus
    return NGUIBase._getMouseFocus(self, position)
  
  
  
  # HIERARCHY
  
  def addChild(self, child):
    child.setParent(self)
    self._children.append(child)
  
  def removeChild(self, child):
    child.setParent(None)
    self._children.remove(child)
 
  def clear(self):
    self._children = []
  
  # DRAWING
  
  def draw(self, view):
    if self._background != None:
      self._background.position = (self._ax, self._ay)
      view.drawSprite(self._background)
    for child in self._children:
      child.draw(view)
    NGUIBase.draw(self, view)
    



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
    




class NGUIBasicButton(NGUIBase):
  def __init__(self, x, y, w, h, text):
    NGUIPane.__init__(self, x, y, w, h)
    self._primed = False
    
    self.text = text
    self.backgroundColour = Color(155,155,155)
    self.outlineColour = Color(200,200,200)
    self.style = "default"
    
    self.backgroundColourFocus = Color(180,180,180)
    self.outlineColourFocus = Color(230,230,230)
    self.styleFocus = "default_focus"
    
    self.backgroundColourPrimed = Color(100,100,100)
    self.outlineColourPrimed = Color(150,150,150)
    self.stylePrimed = "default"
    
    self._margin = 2
    
    # So that whenever the button is defocused, it is also unprimed.
    self.addListener(self)
  
  def packToText(self, margin = 4):
    """Packs the box around the text default, with given margin."""
    self._margin = margin
    textSprite = TextManager.renderText(self.text, self.style)
    rect = textSprite.local_bounds
    self._w = rect.width + self._margin*2
    self._h = rect.height + self._margin*2
  
  
  def onMouseDownEvent(self, event):
    self._primed = True
    
  def onMouseUpEvent(self, event):
    self._primed = False
  
  def onMouseDefocusEvent(self, event):
    self._primed = False
  
  
  def draw(self, view):
    if self._primed:
      self.drawButton(view, self.backgroundColourPrimed, self.outlineColourPrimed, self.stylePrimed)
    elif self._mouseFocus: # Not primed, but focused
      self.drawButton(view, self.backgroundColourFocus, self.outlineColourFocus, self.styleFocus)
    else:
      self.drawButton(view, self.backgroundColour, self.outlineColour, self.style)
  
  def drawButton(self, view, bacgroundColour, outlineColour, style):
    r = RectangleShape()
    r.outline_color = outlineColour
    r.outline_thickness = 1
    r.fill_color = bacgroundColour
    r.position = (self._ax, self._ay)
    r.size = (self._w, self._h)
    view.drawSprite(r)
    
    textSprite = TextManager.renderText(self.text, style)
    rect = textSprite.local_bounds
    # Needs rect.left and stuff because text local bounds are apparently non-0.
    # Something to do with text alignment, perhaps? :)
    textSprite.position = (self._ax + self._w // 2 - (rect.width // 2) - rect.left,
                           self._ay + self._h // 2 - (rect.height // 2) - rect.top)

    view.drawSprite(textSprite)
    


class NGUIImage(NGUIBase):
  def __init__(self, x, y, sprite):
    (w, h) = sprite.local_bounds.size
    self._sprite = sprite
    NGUIPane.__init__(self, x, y, w, h)
  
  def draw(self, view):
    self._sprite.position = (self._ax, self._ay)
    view.drawSprite(self._sprite)




class DebugEventListener:
  def __init__(self, base):
    self._base = base 
  
  def onKeyboardEvent(self, event):
    print("["+self._base.name+"] onKeyboardEvent - " + str(event.code))
  
  def onMouseWheelEvent(self, event):
    print("["+self._base.name+"] onMouseWheelEvent - " + str(event.delta) + ", " + str(event.position))
  
  def onMouseButtonEvent(self, event):
    print("["+self._base.name+"] onMouseButtonEvent - " + str(event.pressed) + ", " + str(event.button) + ", " + str(event.position))
  
  def onMouseEnterEvent(self, event):
    print("["+self._base.name+"] onMouseEnterEvent - " + str(event.oldPosition) + " -> " + str(event.position))
  
  def onMouseExitEvent(self, event):
    print("["+self._base.name+"] onMouseExitEvent - " + str(event.oldPosition) + " -> " + str(event.position))
  
  def onMouseFocusEvent(self, event):
    print("["+self._base.name+"] onMouseFocusEvent - " + str(event.oldPosition) + " -> " + str(event.position))
  
  def onMouseDefocusEvent(self, event):
    print("["+self._base.name+"] onMouseDefocusEvent - " + str(event.oldPosition) + " -> " + str(event.position))
  
  def onMouseMoveEvent(self, event):
    #print("["+self._base.name+"] onMouseMoveEvent - " + str(event.oldPosition) + " -> " + str(event.position))
    pass


    