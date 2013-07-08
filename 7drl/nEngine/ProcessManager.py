

class Process:
  """A simple process."""
  
  UNINITIALISED = 0
  RUNNING = 1
  SUCCESS = 2
  FAIL = 3
  ABORT = 4
  
  def __init__(self):
    """Initialises data. Call this!"""
    self.state = Process.UNINITIALISED
    self.childProcesses = []
  
  def onInit(self):
    """Called when process starts running. Call this!"""
    self.state = Process.RUNNING
    
  def run(self, dt):
    """Run the process again. Implement!
       dt is how much time passed since last call."""
    #TODO: dt being true hinges on the fact that the time each process takes is
    #      constant, and it might be variable. That could lead to some strange
    #      behaviour, maybe?
  
  def onFail(self):
    """Run upon failure. Reimplement."""
  
  def onSuccess(self):
    """Run upon success. Reimplement."""
  
  def onAbort(self):
    """Run upon success. Reimplement."""

  def attachChild(self, process):
    """Attaches a child to execute if this process succeeds."""
    self.childProcesses.append(process)
  
  def removeChild(self, process):
    """Removes child process."""
    self.childProcesses.remove(process)

  def abort(self):
    self.state = Process.ABORT
  def succeed(self):
    self.state = Process.SUCCESS
  def fail(self):
    self.state = Process.FAIL



class ProcessManager:
  """This class maintains a list of processes and manages their execution."""
  
  def __init__(self):
    """Initialises process list."""
    self.processList = []
  
  def run(self, dt):
    """Tells all processes to run.
    dt: how much timed passed since last call."""
  
    toRemove = []
    toAdd = []
    for process in self.processList:
      if process.state == Process.UNINITIALISED:
        process.onInit()
      
      if process.state == Process.RUNNING:
        process.run(dt)
      
      if process.state == Process.SUCCESS:
        process.onSuccess()
        toRemove.append(process)
        toAdd.extend(process.childProcesses)
      elif process.state == Process.FAIL:
        process.onFail()
        toRemove.append(process)
      elif process.state == Process.ABORT:
        process.onAbort()
        toRemove.append(process)
    
    # Populate the old list with the elements that aren't meant to be removed 
    self.processList[:] = [p for p in self.processList if p not in toRemove]
    self.processList.extend(toAdd) # add child processes
  
  
  
  
  
  
  
  
  