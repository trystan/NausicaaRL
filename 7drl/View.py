import pygame

from Utility import Utility

"""This is the View in the MVC paradigm. It is a singleton that handles all
drawing and all sorts of things."""

class View:

  # Stores all images using an identifier
  _images = {}


  @staticmethod
  def init(graphicsRoot):
    """Given the graphics element of the configuration file, parses the
    properties therein and sets them as properties of the View class."""
    for configNode in graphicsRoot:
      setattr(View, configNode.tag, Utility.convert(configNode.text))
  
    """Initialises PyGame and Font, and stuff."""
    pygame.init()
    pygame.font.init()
    
    # Initialises base game font and sets up basic text information
    View.FONT = pygame.font.Font("courbd.ttf", 12)
    View.TITLE_FONT = pygame.font.Font("courbd.ttf", 32)
    View.TEXT_WIDTH, View.TEXT_HEIGHT = View.FONT.size("a")
    
    # Sets up variables specifying the map's space and position. This includes
    # space necessary for the tiles themselves, as well as a border
    View.MapX = 0
    View.MapY = 0
    View.MapW = View.DISPLAY_TILES_X*View.TILE_WIDTH + 2*View.TEXT_HEIGHT
    View.MapH = View.DISPLAY_TILES_Y*View.TILE_HEIGHT + 2*View.TEXT_HEIGHT
    
    # Window width and height are the size of the map frame plus menus
    View.WINDOW_WIDTH = View.MapW + View.RIGHT_MENU_SIZE
    View.WINDOW_HEIGHT = View.MapH + View.BOTTOM_MENU_SIZE
    
    # Creates screen
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    View.screen = pygame.display.set_mode((View.WINDOW_WIDTH,
                                           View.WINDOW_HEIGHT), flags) # Init screen
    pygame.display.set_caption("NausicaaRL") # Set caption
    
    # Create background (to clear image)
    View.background = View.generateBackground(View.screen.get_size())
    

  
  
  @staticmethod
  def generateBackground(size, colour=(0,0,0)):
    """Generates a surface of given size and colour."""
    surface = pygame.Surface(size).convert()
    surface.fill(colour)
    return surface
  
  @staticmethod
  def getImage(sourcefile):
    """Gets the spritesheet in ready-to-use format!"""
    if not sourcefile in View._images:
      image = pygame.image.load(sourcefile)
      View._images[sourcefile] = image
    
    return View._images[sourcefile]
  
  @staticmethod
  def scaleToWindow(surface):
    """Scales the image to fit right into a background."""
    (w, h) = surface.get_size()
    surfaceAspectRatio = w / h
    windowAspectRatio = View.WINDOW_WIDTH / View.WINDOW_HEIGHT
    if surfaceAspectRatio > windowAspectRatio:
      scaleRatio = View.WINDOW_HEIGHT / h
    else:
      scaleRatio = View.WINDOW_WIDTH / w
    
    scaledSurface = pygame.transform.smoothscale(surface,
                                                 (int(w*scaleRatio),
                                                  int(h*scaleRatio)))
    return scaledSurface
  
  @staticmethod
  def limitText(text, width):
    """If the rendered text is longer than width, it returns a new string which
    fits in the required width, with ellipsis (...) at the end."""
    if len(text)*View.TEXT_WIDTH <= width:
      return text
      
    availableSpace  = width - View.TEXT_WIDTH*3
    return text[:(availableSpace//View.TEXT_WIDTH)] + "..."
  
  @staticmethod
  def renderText(text, AA=True, colour=(255,255,255), background=None):
    """Returns a surface with the text rendered."""
    return View.FONT.render(text, AA, colour, background)
  
  @staticmethod
  def renderTitleText(text, AA=True, colour=(255,255,255), background=None):
    """Returns a surface with the text rendered."""
    return View.TITLE_FONT.render(text, AA, colour, background)
  
  @staticmethod
  def renderWrappedText(width, text, AA=True, colour=(255,255,255), background=None):
    """Renders text but wraps it so it doesn't exceed width. Returns a list of
    surfaces containing each line of the text."""
    
    maxTextWidth = width // View.TEXT_WIDTH
    surfaces = []
    while len(text) > maxTextWidth:
      line = text[:maxTextWidth]
      surfaces.append(View.renderText(line, AA, colour, background))
      text = text[maxTextWidth:]
    surfaces.append(View.renderText(text, AA, colour, background))
    
    return surfaces
  
  @staticmethod
  def draw(surface, pos, area=None):
    """Draws a surface on the screen. Should probably not be used directly."""
    View.screen.blit(surface, pos, area)
  
  @staticmethod
  def drawLine(colour, startPos, endPos, width=1):
    pygame.draw.line(View.screen, colour, startPos, endPos, width)
    
  @staticmethod
  def flip():
    pygame.display.flip()
    View.draw(View.background, (0,0))
    
  