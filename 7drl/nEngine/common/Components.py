from nEngine.Entities import Component

class PositionComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.x = None
    self.y = None
  
  
class VelocityComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.vMax = None    
    self.vx = None
    self.vy = None
    
    
class HPComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.HP = None
    self.HPMax = None
  
  def init(self, XMLRoot):
    Component.init(self, XMLRoot)
    self.HP = self.HPMax
  