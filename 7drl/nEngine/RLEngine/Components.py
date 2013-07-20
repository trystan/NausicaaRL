from nEngine.Entities import Component

# The variables indicated in the  components' __init__() functions indicate
# what variables are "expected" in the XML

class PositionComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.posX = None
    self.posY = None
  
  def postInit(self):
    pass



class TileComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.contents = []
    self.roughness = None
  
  def postInit(self):
    pass

    
class BodyComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.parts = []

  def init(self, XMLRoot):
    """Since this is hierarchical stuff, reimplementation is necessary."""
    partNodes = XMLRoot.findAll("PartComponent")
    for partNode in partNodes:
      part = PartComponent(self.entity, self)
      part.init(partNode)
      self.parts.append(part)
  
  def postInit(self):
    for part in self.parts:
      part.postInit()

  def addPart(self, part):
    self.parts.append(part)




class PartComponent(Component):
  """Part components are always part of a body"""
  def __init__(self, entity, parent):
    Component.__init__(self, entity)
    self.parent = parent
  
  def postInit(self):
    pass



class EquipmentComponent(Component):
  def __init__(self, entity):
    Component.__init__(self, entity)
    self.body = None
    self.equipment = {} # Maps parts to the equipment there 
  
  def postInit(self):
    if self.entity.getComponent(BodyComponent) == None:
      print("[ERROR] EquipmentComponent could not find BodyComponent!")
  