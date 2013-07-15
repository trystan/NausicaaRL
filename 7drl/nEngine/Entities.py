"""Entity System implementation. Loosely inspired by Artemis."""
from nEngine.Utility import Utility

class Entity:
  
  IDCounter = 0
  
  def __init__(self, world):
    self.id = Entity.IDCounter
    Entity.IDCounter = Entity.IDCounter + 1
    
    self._components = {}
    self._world = world
  
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
  
  def getComponent(self, componentType):
    """Gets a component based on type."""
    for component in self._components:
      if type(component) == componentType:
        return component
    return None
  
  
class Component:
  """Components types provide an interface. They should be subclasses by any
  concrete components of that type. For example, in an FPS you might have ammo
  and health pickups. The pickup interface is unique, and the ID for both the
  concrete health and ammo pickups is the same. This way you can search for the
  pickup component ID."""
  
  def __init__(self, entity):
    # Meaningless ID!
    self.id = None
    self._entity = entity
  
  def init(self, XMLRoot):
    """Initialisation is called before populating with XML data. The basic
    implementation simply dynamically assigns variable names and their values,
    converted to the most sane type found. Reimplement as necessary."""
    for prop in XMLRoot:
      setattr(self, prop.tag, Utility.convert(prop.text))
  
  def postInit(self):
    """Called after all of the actor components have been populated."""
    print("[WARNING] Component.postInit() not reimplemented")


class System:
  """Systems work on entities with a specific combination of components."""
  def __init__(self, world):
    self._world = world
    self._entities = []
    
  def addEntity(self, entity):
    self._entities.append(entity)
  
  def removeEntity(self, entity):
    self._entities.remove(entity)
  
  def applicable(self, entity):
    """This checks whether this system is applicable to the given entity.
    Can be anything you want. Implement it!"""
    print("[ERROR] System.applicable(entity) not implemented.")
    return False
  
  def run(self, dt):
    """Runs the system, with dt time having passed. Implement it!"""
    print("[ERROR] System.run(dt) not implemented.")



class World:
  """The World class manages all entities and systems that work on entities."""
  
  def __init__(self):
    self._entities = []
    self._systems = {} # Maps system type to system itself.
  
  def addEntity(self, entity):
    self._entities.append(entity)
    for _, system in self._systems.items():
      if system.check(entity):
        system.addEntity(entity)
  
  def removeEntity(self, entity):
    self._entities.remove(entity)
    for _, system in self._systems.items():
      if system.check(entity):
        system.removeEntity(entity)
  
  def addSystem(self, system):
    self._systems[type(system)] = system
  
  def removeSystem(self, system):
    del self._systems[type(system)]
  
  
  
  
  
  