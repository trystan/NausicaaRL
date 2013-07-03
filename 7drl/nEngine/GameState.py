import pygame
from time import time
from nEngine.graphics.Display import Display
from nEngine.Input import Input



class GameManager:
  """The Game Manager includes functions for managing, unsurprisingly, game
  states."""
  def __init__(self):
    self._currentState = None
  
  def run(self):
    """Runs, well, the game :)"""
    while self._currentState != None:
      self._currentState.initialise()
      self._currentState.run()
      self._currentState.terminate()
      self._currentState = self._currentState.nextState()

class GameState:
  """This class contains a generic game state. States switch between each other
  on occasion."""
  
  def __init__(self):
    # Create menu list
    self.initMenus()
    self._nextState = None
  
  def initialise(self):
    """Sets GameState in a ready-to-run situation. In this case, it registers it
    as an input receiver."""
    Input.addInputListener(self)
  
  def terminate(self):
    """Does final computation on this game state before it is removed. In this
    case it deregisters it as an input receiver."""
    Input.removeInputListener(self)
    for menu in self.menus:
      Input.removeInputListener(menu)
    
  def nextState(self):
    """By default returns no next state."""
    return self._nextState
  
  def draw(self):
    """Draws all the currently open menus."""
    for menu in self.menus:
      menu.draw()
  
  #############
  ### MENUS ###
  #############
  
  def initMenus(self):
    """Initialises necessary data structures for menus"""
    self.menus = []
  
  def addMenu(self, menu, catchesInput=True):
    """Adds the menu to the list of rendering menus and possible registers it as
    an input receiver."""
    self.menus.append(menu)
    if catchesInput:
      Input.addInputListener(menu)
  
  def removeMenu(self, menu):
    """Removes the menu to the list of rendering menus and deregisters it as an
    input receiver (if it is there)."""
    self.menus.remove(menu)
    Input.removeInputListener(menu)
  
  ##############
  ### INPUTS ###
  ##############
  
  
  def processEvent(self, gameEvent):
    """The input listener method that processes inputs."""
    print("[ERROR] GameState.processEvent not implemented.")
  
  def run(self):
    """Execute this state's main loop."""
    self.done = False
    
    frameinterval = 1000 // Display.FPS_LIMIT # milliseconds between frames
    oldTime = 0
    while not self.done:
      curTime = time()
      millisElapsed = int((curTime - oldTime)*1000)
      if(millisElapsed < frameinterval):
        pygame.time.wait(frameinterval - millisElapsed)
      oldTime = time()
      
      self.update(millisElapsed)
      
      #lala = time()
      self.draw()
      #print("LOL: " + str(1000*(time() - lala)))
      
      Display.flip() # redraw
      
      
      Input.processInput(self)
      
  def update(self, dt):
    """Meant to update things according to real time, not game time."""
    
    
    
    
    
    
    
    
    
    
    
    
    