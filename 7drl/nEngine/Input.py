from sfml.window import Keyboard, Mouse, KeyEvent, MouseEvent, MouseWheelEvent, MouseButtonEvent, MouseMoveEvent


class GameEvent:
  """This class represents all the events that might be fired once a key is
  pressed. It also contains information about whether the event has already
  been consumed or not. It's up to the classes that might use events to decide
  if the input is consumed or not."""

  def __init__(self, events):
    self.events = events
    self.consumed = False

class MouseEvent:
  def __init__(self, position):
    self.consumed = False
    self.position = position

class Events:
  """Holds all events/eventnames/etc"""
  
  @staticmethod
  def init():
    Events.types = {}
  
  @staticmethod
  def getTypeList(eventType):
    """Returns list of events of a given type. If it does not exist, it
    initialises it."""
    if not eventType in Events.types:
      Events.types[eventType] = []
    return Events.types[eventType]
    
class Input:
  @staticmethod
  def init(view):
    """Given the root of the keyconfig ElementTree, parses it and configures
    all the keys."""
    
    # Initialise event stuff
    Events.init()
    
    # Store the human view to get and send events
    Input.view = view
    
    # Set initial mouse position
    Input.oldMousePosition = (0, 0)
    
    # Counter will be used to set "enum" values
    counter = 0
    
    # Dictionary to store key-to-event/function
    Input.KeyToEvent = {}
    
    # For each game function
    """for child in root:
      print("Parsing " + child.find("description").text + "...")
      
      # Obtain the variable names in string form
      nameStr = child.find("name").text
      keyStrs = child.find("keys").text.split(",")
      keyStrs = [keyStr.strip() for keyStr in keyStrs]
      
      # Add nameStr, the function name, as an actual variable.
      setattr(Events, nameStr, counter)
      counter = counter + 1
      
      # Go through all keys and associate them to this function
      for keyStr in keyStrs:
        KEY = getattr(Keyboard, keyStr) # Get PyGame key constant
        if not KEY in Input.KeyToEvent:
          Input.KeyToEvent[KEY] = []
        
        Input.KeyToEvent[KEY].append(getattr(Events, nameStr))
      
      # If this event has a type, add it to the respective list
      typeElem = child.find("type")
      if typeElem != None:
        eventType = typeElem.text
        Events.getTypeList(eventType).append(getattr(Events, nameStr))
      """
        
    
  
  @staticmethod
  def containsEventOfType(gameEvent, eventType):
    """Checks whether the game event contains any selection event."""
    typeList = Events.getTypeList(eventType)
    for event in gameEvent.events:
      if event in typeList:
        return event
    return None
    
  @staticmethod
  def selectionToIndex(event):
    """This relies on the selection commands being ordered according to the
    alphabet in the config.xml file!"""
    return event - Events.SELECT_A
    
  
  @staticmethod
  def isEvent(key):
    """Checks whether this key generates any events"""
    return key in Input.KeyToEvent
  
  @staticmethod
  def generateGameEvent(key):
    """Returns events associated with this key"""
    return GameEvent(Input.KeyToEvent[key])
  
  @staticmethod
  def processInput():
    """Processes PyGame input and pushes events onto the input stack"""
    # pygame.event.wait() <--- THIS WILL WAIT FOR AN EVENT! HUZZAH!
    for event in Input.view._window.events:
      if event == KeyEvent and Input.isEvent(event.code):
        gameEvent = Input.generateGameEvent(event.code)
        Input.view.onKeyboardEvent(gameEvent)
      elif event == MouseEvent:
        gameEvent = MouseEvent(Mouse.get_position())
        Input.view.onMouseEvent(gameEvent)
      elif event == MouseWheelEvent:
        gameEvent = MouseEvent(event.position)
        gameEvent.delta = event.delta
        Input.view.onMouseWheelEvent(gameEvent)
      elif event == MouseButtonEvent:
        gameEvent = MouseEvent(event.position)
        if(event.pressed and event.released):
          print("[ERROR] Mouse pressed and released at the same time?!")
        gameEvent.pressed = event.pressed
        gameEvent.button = event.button
        Input.view.onMouseButtonEvent(gameEvent)
      elif event == MouseMoveEvent:
        gameEvent = MouseEvent(event.position)
        gameEvent.oldPosition = Input.oldMousePosition
        Input.view.onMouseMoveEvent(gameEvent)
        Input.oldMousePosition = event.position

      