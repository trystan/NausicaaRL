import sys
from collections import deque
from time import time

class Event:
  """This class represents an event"""
  
  # Bogus event type just so we define the variable.
  NO_EVENT = -1
  
  def __init__(self, timestamp):
    """Defines a default event type and the event timestamp."""
    self.type = Event.NO_EVENT
    self.timestamp = timestamp
  
  #TODO: will need to serialise, to be sent over the interwebs
  
class EventManager:
  """Has a global object, but can also be instantiated. Propagates events to
  registered event listeners."""
  
  _singleton = 0
  
  def __init__(self):
    """Sets up all the listener information."""
    self._callbacks = {}
    self._eventQueue = deque()
    
    
  def _initialiseEventType(self, eventType):
    """Internal function to initialise the lists for specific event types."""
    self._callbacks[eventType] = []
    
  def registerListener(self, eventType, callback):
    """Registers a new listener. Whenever a new event of this type occurs, all
    callbacks from the respective list are called."""
    if not eventType in self._callbacks:
      self._initialiseEventType(eventType)
    
    self._callbacks[eventType].append(callback)
    
  def deregisterListener(self, eventType, callback):
    """Does what it says on the box!"""
    self._callbacks[eventType].remove(callback)
    
  def queueEvent(self, event):
    """Queues an event to be handled later, in order."""
    self._eventQueue.append(event)
  
  def dequeueEvent(self, event):
    """DEqueues an event..."""
    self._eventQueue.remove(event)
    
  def handleEvent(self, event):
    """Processes all callbacks related to this event. This will be instant!
    Normally, queueEvent should be called, and EventManager.handleEvents will
    eventually take care of it."""
    callbacks  = self._callbacks[event.type]
    for callback in callbacks:
      callback(event)
  
  def handleEvents(self, maxTime = sys.maxsize):
    """Processes the event queue, until maxTime is reached."""
    startTime = time()
    while len(self._eventQueue) > 0 and time() - startTime < maxTime:
      event = self._eventQueue.popleft()
      self.handleEvent(event)
      
  @staticmethod
  def getEM():
    """Gets the global, singleton event manager."""
    if EventManager._singleton == 0:
      EventManager._singleton = EventManager()
    
    return EventManager._singleton
    
    
    
    
    
    
    