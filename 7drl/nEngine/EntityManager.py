import copy
import xml.etree.ElementTree as ElementTree

from nEngine.model.GameModel import *
from nEngine.graphics.Graphics import Animation, DisplayBlueprint, Frame
from nEngine.graphics.Display import Display
from nEngine.Utility import Utility

"""This module will read the data in the XML files and handle loading of
graphics and of base information for each type of entity."""

class Blueprint:
  """A blueprint contains all the information and variables about one type of
  entity. It stores the class it constructs."""
  
  # A counter to uniquely identify each blueprint.
  counter = 0
  
  def __init__(self, attribs, ClassConstructed):
    # Dynamically set class variables and values based on attribs
    self.ClassConstructed = ClassConstructed
    for (varName, varValue) in attribs.items():
      setattr(self, varName, varValue)
      
    # Add identifier
    self.id = Blueprint.counter
    Blueprint.counter = Blueprint.counter + 1

  def construct(self, parent):
    """Constructs an entity within a parent. For most things, parent will be the
    world. For others, like parts, it will be the actor they belong to."""
    return self.ClassConstructed(self, parent)


class EntityManager:
  """The entity manager parses the entities file and builds up the blueprints
  for all of the entities.
  
  It stores all of the blueprints inside a dictionary indexed by blueprint
  name. Similarly for spritesheets.
  
  It's a singleton."""
  
  blueprints = {}
  
  @staticmethod
  def construct(entityName, world):
    """Construct an object given by this entity name."""
    return EntityManager.blueprints[entityName].construct(world)
    
  @staticmethod  
  def parseFile(filename):
    """This function parses all entities from the given filename."""
    
    print("Parsing entities.")
    
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    
    order = ("tiles", "parts", "objects", "containers", "actors", "heros", "crops", "doors")
    entityTypes = {"tiles":Tile, "parts":Part, "objects":Object, 
                   "containers":Container, "actors":Actor, "heros":Hero,
                   "crops":Crop, "doors":Door}
    
    for entityType in order:
      EntityManager.parseEntityType(root, entityType, entityTypes[entityType])

  @staticmethod
  def parseEntityType(root, entityClass, ClassConstructed):
    """Given the root of the XML tree, the class of items to parse and the class
    that they construct, reads default variable values and each blueprint of
    that type."""
    # Get the tree for all entities of that class
    entityClassNode = root.find(entityClass)
    
    # Initialise attribute tree with default values
    attribs = EntityManager.parseDefaultAttributes(root, entityClassNode)
    
    # Parse actual blueprints
    for entityType in entityClassNode.findall("entity"):
      print("Parsing " + entityType.find("name").text)
      # Copy default attribs
      entityAttribs = copy.deepcopy(attribs)
      # Parse blueprint 
      EntityManager.parseBlueprint(entityType, entityAttribs, ClassConstructed)
  
  @staticmethod
  def parseDefaultAttributes(root, classRoot):
    """Receives the root of the document, and the root of the class node.
    Returns an attribs dictionary with parsed default values, including checking
    superclasses."""
    
    # Check superclass for default values
    if "superclass" in classRoot.attrib:
      superclass = classRoot.attrib["superclass"]
      superclassRoot = root.find(superclass)
      if superclassRoot == None:
        print("[ERROR] Could not find superclass for " + classRoot.tag)
        return -1
      attribs = EntityManager.parseDefaultAttributes(root, superclassRoot)
    else:
      attribs = {}
      
    # Find default node
    defaultNode = classRoot.find("default")
    if defaultNode == None:
      return attribs
    
    # There are default values
    for defaultProperty in defaultNode:
      attribs[defaultProperty.tag] = Utility.convert(defaultProperty.text)
    
    return attribs
    
  
  @staticmethod 
  def parseBlueprint(root, attribs, ClassConstructed):
    """Parses all the components of any blueprint. Guesses the types of each
    attribute. Puts them in attribs. Attribs may contain peanuts. Just kidding,
    it may contain default values. In fact, it should, for actors."""
    
    # Go through all sub-elements and make them attributes
    for child in root:
      if child.tag == "display":
        attribs[child.tag] = EntityManager.parseDisplayInfo(child)
      elif child.tag == "parts":
        attribs[child.tag] = EntityManager.parseIntoBlueprints(child)
      elif child.tag == "equipAt":
        print(child)
        attribs[child.tag] = EntityManager.parseIntoBlueprintIDs(child)
      else:
        attribs[child.tag] = Utility.convert(child.text)
    
    EntityManager.blueprints[attribs["name"]] = Blueprint(attribs, ClassConstructed)
  
  @staticmethod
  def parseIntoBlueprints(root):
    """Given the root of an XML element with a list of entities, returns a list
    with their respective blueprints."""
    partBPList = []
    names = Utility.convert(root.text)
    for name in names:
      if not name in EntityManager.blueprints:
        print("[ERROR] Unknown part: " + name)
        return None
      partBPList.append(EntityManager.blueprints[name])
      
    return partBPList
    
  @staticmethod
  def parseIntoBlueprintIDs(root): 
    """Given the root of an XML element with a list of entities, returns a list
    with their respective blueprints IDs."""
    print(root)
    return [bp.id for bp in EntityManager.parseIntoBlueprints(root)]
  
  
  @staticmethod
  def parseDisplayInfo(root):
    """Parses all display information from one display subtree."""
    
    attribs = {}
    for child in root:
      if child.tag == "animation":
        continue
      attribs[child.tag] = Utility.convert(child.text)
    
    attribs["animations"] = [EntityManager.parseAnimation(child) for child in root.findall("animation")]
    return DisplayBlueprint(**attribs)
  
  @staticmethod
  def parseAnimation(root):
    """Parses a single animation."""
    
    # By default, dx and dy are 0!
    attribs = {"dx": 0, "dy": 0}
    for child in root:
      if child.tag == "frame":
        continue
      attribs[child.tag] = Utility.convert(child.text)

    attribs["frames"] = [EntityManager.parseFrame(child) for child in root.findall("frame")]
    
    # Deal with spritesheet
    attribs["spritesheet"] = Display.getImage(attribs["spritesheet"])
    
    return Animation(**attribs)
  
  
  @staticmethod
  def parseFrame(root):
    """Simply parses a frame."""
    attribs = {}
    for child in root:
      attribs[child.tag] = Utility.convert(child.text)
    
    # Use dictinary to determine all the init parameters \o/
    return Frame(**attribs)
    
  
  
  
  
  
  