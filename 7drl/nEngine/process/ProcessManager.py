

class Process:
  """A simple process."""
  
  UNINITIALISED = 0
  
  def __init__(self):
    self.state = Process.UNINITIALISED

class ProcessManager:
  """This class maintains a list of processes and manages their execution."""
  
  