from nEngine.Entities import Component, EntityFactory

class DamageComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.damage = None

class BulletCollisionComponent(Component):
  pass
  
class RangeComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.range = None
  
  def init(self, XMLRoot):
    Component.init(self, XMLRoot)
    self.distance = 0

class ShootingComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.timeToReload = 0
  

class WeaponComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    
  def init(self, XMLRoot):
    Component.init(self, XMLRoot)
    self.weapon = EntityFactory.getSingleton().produce(self._entity.world, self.weaponName)
  