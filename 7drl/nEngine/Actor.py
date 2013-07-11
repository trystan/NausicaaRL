"""Actors are two things:
- Component sets
- Event managers

Components will mostly communicate through the event system, but can also
communicate directly, by asking if there is another specific component around.

The event-based system, of course, promotes more reusability.
"""

from nEngine.EventManager import EventManager

class Actor (EventManager):
  """An actor is simply a map of components whose key is an interface type."""
  
  IDCounter = 0
  
  def __init__(self):
    self.id = Actor.IDCounter
    Actor.IDCounter = Actor.IDCounter + 1
    
    self._components = {}
  
  def init(self, XMLRoot):
    """Do stuff with data that is not components..."""
    self.name = XMLRoot.find("name").text
  
  def addComponent(self, component):
    """Adds component to component map..."""
    if not component.id in self._components:
      self._components[component.id] = []
    
    self._components[component.id].append(component)
  
  def run(self, dt):
    """Time has passed. Work!"""
    for component in self._components:
      component.run(dt)
  
  
class Component:
  """Components types provide an interface. They should be subclasses by any
  concrete components of that type. For example, in an FPS you might have ammo
  and health pickups. The pickup interface is unique, and the ID for both the
  concrete health and ammo pickups is the same. This way you can search for the
  pickup component ID."""
  
  def __init__(self, parent):
    # Meaningless ID!
    self.id = None
    self._parent = parent
  
  def init(self, XMLRoot):
    """Initialisation is called before populating with XML data. Reimplement.
       Probably not a bad place to set up listeners on self._parent!"""
    print("[WARNING] Component.init(XMLroot) not reimplemented")
  
  def postInit(self):
    """Called after all of the actor components have been populated."""
    print("[WARNING] Component.postInit() not reimplemented")
  
  def run(self, dt):
    """Time has passed. Work!"""
    print("[WARNING] Component.run() not reimplemented")