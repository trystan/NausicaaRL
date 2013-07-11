import sfml

from nEngine.Utility import Utility

"""This is the View in the MVC paradigm. It is a singleton that handles all
drawing and all sorts of things."""

class Display:

  # Stores all images using an identifier
  _textures = {}


  @staticmethod
  def init(graphicsRoot):
    """Given the graphics element of the configuration file, parses the
    properties therein and sets them as properties of the View class."""
    for configNode in graphicsRoot:
      setattr(Display, configNode.tag, Utility.convert(configNode.text))
      
    # Creates screen
    Display.screen = sfml.RenderWindow(sfml.VideoMode(Display.WINDOW_WIDTH, Display.WINDOW_HEIGHT), "NausicaaRL")

    
  
  @staticmethod
  def getTexture(sourcefile):
    """Gets the spritesheet in ready-to-use format!"""
    if not sourcefile in Display._textures:
      image = sfml.Texture.from_file(sourcefile)
      Display._textures[sourcefile] = image
    
    return Display._textures[sourcefile]
  
  @staticmethod
  def scaleToWindow(sprite):
    """Scales the sprite to fit right into a background."""
    (w, h) = sprite.local_bounds.size
    surfaceAspectRatio = w / h
    windowAspectRatio = Display.WINDOW_WIDTH / Display.WINDOW_HEIGHT
    if surfaceAspectRatio > windowAspectRatio:
      scaleRatio = Display.WINDOW_HEIGHT / h
    else:
      scaleRatio = Display.WINDOW_WIDTH / w
    
    sprite.scale(scaleRatio)
    
    return sprite
  
  @staticmethod
  def draw(sprite):
    """Draws a surface on the screen. Should probably not be used directly."""
    Display.screen.draw(sprite)
  
  @staticmethod
  def drawLine(colour, startPos, endPos, width=1):
    lines = sfml.VertexArray(sfml.PrimitiveType.LINES_STRIP, 2)
    lines[0].position = startPos
    lines[1].position = endPos
    Display.screen.draw(lines)
    
  @staticmethod
  def clear(colour = sfml.Color.BLACK):
    Display.screen.clear(colour)
    
  