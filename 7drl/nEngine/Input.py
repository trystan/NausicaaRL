import pygame.locals
from pygame.locals import KEYDOWN 


class GameEvent:
  """This class represents all the events that might be fired once a key is
  pressed. It also contains information about whether the event has already
  been consumed or not. It's up to the classes that might use events to decide
  if the input is consumed or not."""

  def __init__(self, events):
    self.events = events
    self.consumed = False

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
  def init(root):
    """Given the root of the keyconfig ElementTree, parses it and configures
    all the keys."""
    
    # Initialise event stuff
    Events.init()
    
    # Initialise input stack
    Input.stack = []
    
    # Counter will be used to set "enum" values
    counter = 0
    
    # Dictionary to store key-to-event/function
    Input.KeyToEvent = {}
    
    # For each game function
    for child in root:
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
        KEY = getattr(pygame.locals, keyStr) # Get PyGame key constant
        if not KEY in Input.KeyToEvent:
          Input.KeyToEvent[KEY] = []
        
        Input.KeyToEvent[KEY].append(getattr(Events, nameStr))
      
      # If this event has a type, add it to the respective list
      typeElem = child.find("type")
      if typeElem != None:
        eventType = typeElem.text
        Events.getTypeList(eventType).append(getattr(Events, nameStr))
        
    
  
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
  def processInput(gameState):
    """Processes PyGame input and pushes events onto the input stack"""
    # pygame.event.wait() <--- THIS WILL WAIT FOR AN EVENT! HUZZAH!
    for event in pygame.event.get():
      if event.type == KEYDOWN and Input.isEvent(event.key):
        gameEvent = Input.generateGameEvent(event.key)
        Input.processEvent(gameEvent)
      
  @staticmethod
  def processEvent(gameEvent):
    """Processes a single event through the input stack."""
    for inputListener in reversed(Input.stack):
      inputListener.processEvent(gameEvent)
      if gameEvent.consumed:
        break
  
  @staticmethod
  def addInputListener(listener):
    """Registers listener as ready to receive input. Works as a stack, so the 
    latest listeners will have a chance to consume input earlier."""
    Input.stack.append(listener)
  
  @staticmethod
  def removeInputListener(listener):
    """Deregisters a listener. Doesn't need to be the latest one to be
    registered, in case someone wants to have multiple menus open."""
    if listener in Input.stack:
      Input.stack.remove(listener)
        
        
        
        


        
        
        