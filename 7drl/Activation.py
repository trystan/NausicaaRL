class Activation:
  """Represents something that should be activated at some point."""
  
  counter = 0
  
  def __init__(self, time, function, args = []):
    """Time is the time at which the function should be called, time, function
    is the function to be called, typically a bound class method, and args are
    the arguments it should be called with."""
    self.id = Activation.counter
    Activation.counter = Activation.counter + 1
    
    self.time = time
    self.function = function
    self.args = args
    
  def activate(self):
    """Calls the function."""
    self.function(*self.args)
    
  def __eq__(self, other):
    if other == None:
      return False
    return self.id == other.id
  
  def __lt__(self, other):
    if self.time < other.time:
      return True
    elif self.time > other.time:
      return False
    # They are equal
    return self.id < other.id