


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
    print("[WARNING] Process.run(dt) not reimplemented.")
  
  def onFail(self):
    """Run upon failure. Reimplement."""
    print("[WARNING] Process.onFail(dt) not reimplemented.")
  
  def onSuccess(self):
    """Run upon success. Reimplement."""
    print("[WARNING] Process.onSuccess(dt) not reimplemented.")
  
  def onAbort(self):
    """Run upon success. Reimplement."""
    print("[WARNING] Process.onAbort(dt) not reimplemented.")

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


def RunCallbackProcess(Process):
  """This process simply handles a list of callbacks that take one argument:
  how much time has passed, and calls them."""
  
  def __init__(self):
    self._callbacks = []
  
  def addCallback(self, callback):
    self._callbacks.append(callback)
  def removeCallback(self, callback):
    self._callbacks.remove(callback)

    
  def run(self, dt):
    """Simply iteratse all callbacks and calls them :)"""
    for callback in self._callbacks:
      callback(dt)
    
  def onFail(self): None
  def onSuccess(self): None
  def onAbort(self): None
  
    
    
    
    
    
      
  
  
  
  
  