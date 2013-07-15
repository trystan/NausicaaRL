from nEngine.Input import *


class Utility:
  """Contains several static methods that are generally useful."""
  
  @staticmethod
  def toBoolean(text):
    """Converts text to boolean."""
    return text.lower() == "true"
    
  @staticmethod
  def convert(text):
    """Guesses the type and text to a value of that type."""
    if text == "[]":
      return []
      
    if text == None:
      return ""
      
    if Utility.isInt(text):
      return int(text)
      
    if Utility.isFloat(text):
      return float(text)
    
    if text.lower() == "true":
      return True
    
    if text.lower() == "false":
      return False
      
    if text.lower() == "none":
      return None

    # TODO: Does not work for list of lists...
    if text[0] == "[" and text[len(text)-1] == "]":
      foundIndex = text.find(",")
      if foundIndex == -1:
        return [Utility.convert(text[1:-1])]
      else:
        text = text[1:-1]
        tokens = text.split(",")
        return [Utility.convert(elem.strip()) for elem in tokens]
    
    return text
  
  @staticmethod
  def isInt(text):
    """Checks whether the text represents an int."""
    try: 
      int(text)
      return True
    except ValueError:
      return False
    except TypeError:
      return False

  @staticmethod
  def isFloat(text):
    """Checks whether the text represents a float."""
    try: 
      float(text)
      return True
    except ValueError:
      return False
    except TypeError:
      return False
        
  @staticmethod
  def entitiesToText(entityList):
    """Concatenates the names of entities."""
    return ", ".join([entity.blueprint.name for entity in entityList])
    
    
  @staticmethod
  def movementEventToVector(event):
    """Takes the event and returns the (dx, dy) coordinates related to its
    movement. For CLIMB and DESCEND, it returns (-2,-2) and (+2, +2) respectively."""
    if event == Events.MOVE_UP:
      return (0, -1)
    elif event == Events.MOVE_UP_LEFT:
      return (-1,-1)
    elif event == Events.MOVE_LEFT:
      return (-1, 0)
    elif event == Events.MOVE_DOWN_LEFT:
      return (-1, 1)
    elif event == Events.MOVE_DOWN:
      return ( 0, 1)
    elif event == Events.MOVE_DOWN_RIGHT:
      return ( 1, 1)
    elif event == Events.MOVE_RIGHT:
      return ( 1, 0)
    elif event == Events.MOVE_UP_RIGHT:
      return ( 1, -1)
    elif event == Events.WAIT:
      return ( 0, 0)
    elif event == Events.CLIMB:
      return (-2,-2)
    elif event == Events.DESCEND:
      return ( 2, 2)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      