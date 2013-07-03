import pygame

from nEngine.Utility import Utility

"""This is the View in the MVC paradigm. It is a singleton that handles all
drawing and all sorts of things."""

class Display:

  # Stores all images using an identifier
  _images = {}


  @staticmethod
  def init(graphicsRoot):
    """Given the graphics element of the configuration file, parses the
    properties therein and sets them as properties of the View class."""
    for configNode in graphicsRoot:
      setattr(Display, configNode.tag, Utility.convert(configNode.text))
  
    """Initialises PyGame and Font, and stuff."""
    pygame.init()
    pygame.font.init()
    
    # Initialises base game font and sets up basic text information
    Display.FONT = pygame.font.Font("data/courbd.ttf", 12)
    Display.TITLE_FONT = pygame.font.Font("data/courbd.ttf", 32)
    Display.TEXT_WIDTH, Display.TEXT_HEIGHT = Display.FONT.size("a")
    
    # Sets up variables specifying the map's space and position. This includes
    # space necessary for the tiles themselves, as well as a border
    Display.MapX = 0
    Display.MapY = 0
    Display.MapW = Display.DISPLAY_TILES_X*Display.TILE_WIDTH + 2*Display.TEXT_HEIGHT
    Display.MapH = Display.DISPLAY_TILES_Y*Display.TILE_HEIGHT + 2*Display.TEXT_HEIGHT
    
    # Window width and height are the size of the map frame plus menus
    Display.WINDOW_WIDTH = Display.MapW + Display.RIGHT_MENU_SIZE
    Display.WINDOW_HEIGHT = Display.MapH + Display.BOTTOM_MENU_SIZE
    
    # Creates screen
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    Display.screen = pygame.display.set_mode((Display.WINDOW_WIDTH,
                                           Display.WINDOW_HEIGHT), flags) # Init screen
    pygame.display.set_caption("NausicaaRL") # Set caption
    
    # Create background (to clear image)
    Display.background = Display.generateBackground(Display.screen.get_size())
    

  
  
  @staticmethod
  def generateBackground(size, colour=(0,0,0)):
    """Generates a surface of given size and colour."""
    surface = pygame.Surface(size).convert()
    surface.fill(colour)
    return surface
  
  @staticmethod
  def getImage(sourcefile):
    """Gets the spritesheet in ready-to-use format!"""
    if not sourcefile in Display._images:
      image = pygame.image.load(sourcefile)
      Display._images[sourcefile] = image
    
    return Display._images[sourcefile]
  
  @staticmethod
  def scaleToWindow(surface):
    """Scales the image to fit right into a background."""
    (w, h) = surface.get_size()
    surfaceAspectRatio = w / h
    windowAspectRatio = Display.WINDOW_WIDTH / Display.WINDOW_HEIGHT
    if surfaceAspectRatio > windowAspectRatio:
      scaleRatio = Display.WINDOW_HEIGHT / h
    else:
      scaleRatio = Display.WINDOW_WIDTH / w
    
    scaledSurface = pygame.transform.smoothscale(surface,
                                                 (int(w*scaleRatio),
                                                  int(h*scaleRatio)))
    return scaledSurface
  
  @staticmethod
  def limitText(text, width):
    """If the rendered text is longer than width, it returns a new string which
    fits in the required width, with ellipsis (...) at the end."""
    if len(text)*Display.TEXT_WIDTH <= width:
      return text
      
    availableSpace  = width - Display.TEXT_WIDTH*3
    return text[:(availableSpace//Display.TEXT_WIDTH)] + "..."
  
  @staticmethod
  def renderText(text, AA=True, colour=(255,255,255), background=None):
    """Returns a surface with the text rendered."""
    return Display.FONT.render(text, AA, colour, background)
  
  @staticmethod
  def renderTitleText(text, AA=True, colour=(255,255,255), background=None):
    """Returns a surface with the text rendered."""
    return Display.TITLE_FONT.render(text, AA, colour, background)
  
  @staticmethod
  def renderWrappedText(width, text, AA=True, colour=(255,255,255), background=None):
    """Renders text but wraps it so it doesn't exceed width. Returns a list of
    surfaces containing each line of the text."""
    
    maxTextWidth = width // Display.TEXT_WIDTH
    surfaces = []
    while len(text) > maxTextWidth:
      line = text[:maxTextWidth]
      surfaces.append(Display.renderText(line, AA, colour, background))
      text = text[maxTextWidth:]
    surfaces.append(Display.renderText(text, AA, colour, background))
    
    return surfaces
  
  @staticmethod
  def draw(surface, pos, area=None):
    """Draws a surface on the screen. Should probably not be used directly."""
    Display.screen.blit(surface, pos, area)
  
  @staticmethod
  def drawLine(colour, startPos, endPos, width=1):
    pygame.draw.line(Display.screen, colour, startPos, endPos, width)
    
  @staticmethod
  def flip():
    pygame.display.flip()
    Display.draw(Display.background, (0,0))
    
  