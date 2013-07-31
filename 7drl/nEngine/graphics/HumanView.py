import sfml

import xml.etree.ElementTree as ElementTree

from nEngine.Utility import Utility
from nEngine.Input import Input
from nEngine.graphics.nGUI import NGUIPane
from nEngine.graphics.TextManager import TextManager

"""This is the View in the MVC paradigm. It is a singleton that handles all
drawing and all sorts of things."""

class HumanView():

  # Stores all images using an identifier
  _textures = {}


  def init(self, title, graphicsFile):
    """Given the graphics element of the configuration file, parses the
    properties therein and sets them as properties of the View class."""
    XMLroot = ElementTree.parse(graphicsFile).getroot()
    for configNode in XMLroot:
      setattr(self, configNode.tag, Utility.convert(configNode.text))
    
    Input.init(self)
    TextManager.init()
    
    # Creates screen
    self._window = sfml.RenderWindow(sfml.VideoMode(self.WINDOW_WIDTH, self.WINDOW_HEIGHT), title)
    self._pane = NGUIPane(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
    self._pane.name = "HumanView"
    self.mouseFocus = None
  
  def getPane(self):
    return self._pane

    
  def getTexture(self, sourcefile):
    """Gets the spritesheet in ready-to-use format!"""
    if not sourcefile in self._textures:
      image = sfml.Texture.from_file(sourcefile)
      self._textures[sourcefile] = image
    
    return self._textures[sourcefile]
  
  
  def scaleToWindow(self, sprite):
    """Scales the sprite to fit right into a background."""
    (w, h) = sprite.local_bounds.size
    surfaceAspectRatio = w / h
    windowAspectRatio = self.WINDOW_WIDTH / self.WINDOW_HEIGHT
    if surfaceAspectRatio > windowAspectRatio:
      scaleRatio = self.WINDOW_HEIGHT / h
    else:
      scaleRatio = self.WINDOW_WIDTH / w
    
    sprite.scale(scaleRatio)
    
    return sprite
  
  
  def draw(self):
    self.clear()
    self._pane.draw(self)
    self._window.display()

  def drawSprite(self, sprite):
    """Draws a surface on the screen. Should probably not be used directly."""
    self._window.draw(sprite)
  
  def drawLine(self, colour, startPos, endPos, width=1):
    #TODO: Line width not implemented yet
    lines = sfml.VertexArray(sfml.PrimitiveType.LINES_STRIP, 2)
    lines[0].position = startPos
    lines[0].color = colour
    lines[1].position = endPos
    lines[1].color = colour
    self._window.draw(lines)
    
  def clear(self, colour = sfml.Color.BLACK):
    self._window.clear(colour)
  
  # Input
  
  def onKeyboardEvent(self, event):
    pass
  
  def onMouseEvent(self, event):
    print("[WARNING] HumanView.onMouseEvent called. This has never happened before!")
  
  def onMouseWheelEvent(self, event):
    self._pane._onMouseWheelEvent(event)
  
  def onMouseButtonEvent(self, event):
    self._pane._onMouseButtonEvent(event)
  
  def onMouseMoveEvent(self, event):
    self._pane._onMouseMoveEvent(event)
    newFocus = self._pane._getMouseFocus(event.position)
    if newFocus != self.mouseFocus:
      if self.mouseFocus != None:
        self.mouseFocus._onMouseDefocusEvent(event)
      self.mouseFocus = newFocus
      self.mouseFocus._onMouseFocusEvent(event)
    
  
  