from nEngine.Events import Event

class EntityCreatedEvent(Event):
  def __init__(self, entity):
    self.entity = entity
  
  def getClass(self):
    return type(self.entity)

class EntityMovedEvent(Event):
  def __init__(self, entity, origin, destination):
    self.entity = entity
    self.origin = origin
    self.destination = destination