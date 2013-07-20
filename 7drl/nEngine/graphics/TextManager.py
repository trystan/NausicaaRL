import sfml

import xml.etree.ElementTree as ElementTree

class TextStyle:
  """Contains all the options that can be used to customise text rendering."""
  
  def __init__(self, XMLroot):
    """Initialises all the important data."""
    
    self.font = TextManager.fontMap[XMLroot.find("font").text]
    self.size = int(XMLroot.find("size").text)
    self.parseStyle(XMLroot.find("style").text)
    self.parseColour(XMLroot.find("colour").text)
  
  def parseStyle(self, text):
    """Parse and save styles."""
    tokens = [str.strip().upper() for str in text.split(",")]
    self.style = 0
    for token in tokens:
      if token == "REGULAR":
        self.style = self.style | sfml.Text.REGULAR
      elif token == "BOLD":
        self.style = self.style | sfml.Text.BOLD
      elif token == "ITALIC":
        self.style = self.style | sfml.Text.ITALIC
      elif token == "UNDERLINED":
        self.style = self.style | sfml.Text.UNDERLINED
    
  
  def parseColour(self, text):
    """Parse and save styles."""
    tokens = [str.strip() for str in text.split(",")]
    self.colour = sfml.Color(int(tokens[0]), int(tokens[1]), int(tokens[2]))
  
  def getTextSprite(self, text):
    """Returns a sfml.Text with the given text, and its own options."""
    textSprite = sfml.Text(text)
    textSprite.font = self.font
    textSprite.character_size = self.size
    textSprite.style = self.style
    textSprite.color = self.colour
    return textSprite
    
    
    
class TextManager:
  """This class contains all functions related to font loading, options and
  text handling in general."""
  
  @staticmethod
  def init():
    """Initialises the font and option maps."""
    TextManager.optionMap = {}
    TextManager.fontMap = {}
  
  @staticmethod
  def loadFont(XMLroot):
    """Loads a font from file, given the XML root containing the info."""
    fontName = XMLroot.attrib["name"]
    font = sfml.Font.from_file(XMLroot.text)
    TextManager.fontMap[fontName] = font
  
  @staticmethod
  def loadOption(XMLroot):
    """Loads options from the XMLroot."""
    
    name = XMLroot.attrib["name"]
    TextManager.optionMap[name] = TextStyle(XMLroot)
  
  @staticmethod
  def loadFromFile(file):
    """Loads options from an XML tree element."""
    
    XMLroot = ElementTree.parse(file).getroot()
    
    # Load fonts first
    fontsRoot = XMLroot.find("fonts")
    for font in fontsRoot:
      TextManager.loadFont(font)
    
    # Load options
    optionsRoot = XMLroot.find("options")
    for option in optionsRoot:
      TextManager.loadOption(option)
    
    
    
    
    
  @staticmethod
  def renderLimitedText(text, optionName, maxWidth, lineEnd = "..."):
    """If the rendered text is longer than width, it returns a new string which
    fits in the required width, with ellipsis (...), by default, at the end."""
    #TODO: Linear, can probably be made faster.
    option = TextManager.optionMap[optionName]
    # create a text
    textSprite = option.getTextSprite(text)
    
    # If it's too large, add line ender
    if textSprite.local_bounds.width > maxWidth:
      textSprite.string = textSprite.string + lineEnd
    
    # While the text, with line ender, is too large, remove one character
    while textSprite.local_bounds.width > maxWidth:
      textSprite.string = textSprite.string[:(-len(lineEnd)-1)] + lineEnd
      
    return textSprite
  
  @staticmethod
  def renderText(text, optionName):
    """Returns a surface with the text rendered."""
    return TextManager.optionMap[optionName].getTextSprite(text)
  
  @staticmethod
  def renderWrappedText(text, optionName, maxWidth):
    """Renders text but wraps it so it doesn't exceed width. Returns a list of
    surfaces containing each line of the text."""
    
    lines = []
    
    # While there is still text, render limited text, see how much was consumed
    # and then remove that string from the front of the to-render text
    while len(text) > 0:
      line = TextManager.renderLimitedText(text, optionName, maxWidth, "")
      lines.append(line)
      text = text[len(line.string):]
    
    return lines
    
    
    
  