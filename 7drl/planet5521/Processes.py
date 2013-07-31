from nEngine.Processes import Process
from nEngine.Input import Input


class HumanViewProcess(Process):
  def __init__(self, humanView):
    Process.__init__(self)
    self._humanView = humanView
  
    
  def run(self, dt):
    Input.processInput()
    self._humanView.draw()
  


      
  
  
  
  
  