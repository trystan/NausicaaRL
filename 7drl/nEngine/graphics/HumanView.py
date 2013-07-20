import sfml

from nEngine.Utility import Utility

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
    self.window = sfml.RenderWindow(sfml.VideoMode(self.WINDOW_WIDTH, self.WINDOW_HEIGHT), title)

    
  
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
  

  def draw(self, sprite):
    """Draws a surface on the screen. Should probably not be used directly."""
    self.window.draw(sprite)
  
  def drawLine(self, colour, startPos, endPos, width=1):
    lines = sfml.VertexArray(sfml.PrimitiveType.LINES_STRIP, 2)
    lines[0].position = startPos
    lines[1].position = endPos
    self.window.draw(lines)
    
  def clear(self, colour = sfml.Color.BLACK):
    self.window.clear(colour)
  
  # Input
  
  def onKeyboardEvent(self, event):
    print("OnMouseEvent")
    print(str(event.code) + ", " + str(event.pressed) + ", " + str(event.released))
  
  def onMouseEvent(self, event): 
    print("OnMouseEvent")
    print(str(event.entered) + ", " + str(event.left))
  
  def onMouseWheelEvent(self, event):
    print("OnMouseWheelEvent")
    print(str(event.delta) + ", " + str(event.position))
  
  def onMouseButtonEvent(self, event):
    print("OnMouseButtonEvent")
    print(str(event.pressed) + ", " + str(event.released) + ", " + str(event.button) + ", " + str(event.position))
  
  def onMouseMoveEvent(self, event):
    print("OnMouseMoveEvent")
    print(str(event.position) + ", " + str(event.oldPosition))
  