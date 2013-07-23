import sfml

from nEngine.Utility import Utility
from nEngine.Options import Options
from nEngine.graphics.nGUI import NGUIPane

"""This is the View in the MVC paradigm. It is a singleton that handles all
drawing and all sorts of things."""

class HumanView():

  # Stores all images using an identifier
  _textures = {}


  def init(self, title, graphicsRoot):
    """Given the graphics element of the configuration file, parses the
    properties therein and sets them as properties of the View class."""
    for configNode in graphicsRoot:
      setattr(self, configNode.tag, Utility.convert(configNode.text))
      
    # Creates screen
    self._window = sfml.RenderWindow(sfml.VideoMode(self.WINDOW_WIDTH, self.WINDOW_HEIGHT), title)
    self._pane = NGUIPane(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
    self._pane.name = "HumanView"

    
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
    lines[1].position = endPos
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
  
  