from nEngine.GameState import GameState
from nEngine.graphics.Display import *
from nEngine.graphics.nGUI.nGUI import *
from NausicaaRL.NausicaaWorlds import *
from nEngine.Input import *

class TitleScreenState(GameState):
  """This is just the title screen."""
  
  def __init__(self):
    GameState.__init__(self)
    
  def initialise(self):
    """Initialises menus, etc"""
    GameState.initialise(self)
    self.createBackground()
    self.createTitleMenu()
  
  def createBackground(self):
    """Loads the background and sets it up according to resolution."""
    
    # Load background image and scale it so it fits nicely into the window
    background = Display.getImage("data/nausicaa.jpg")
    background = Display.scaleToWindow(background)
    
    # Align its top-right to the top-right of the window
    (w, _) = background.get_size()
    posX = Display.WINDOW_WIDTH - w
    posY = 0
    sprite = Sprite(background, (posX, posY))
    
    # Add this as a non-input listener
    self.addMenu(sprite, False)
    
  
  def createTitleMenu(self):
    """Creates the main menu list."""
    
    menu = ScrollTitleSelector(150,150,100,100,
                              "Main Title",
                              ["Start game", "Exit"], [True, False])
    menu.setCallback(self.mainMenuChoice, [])
    self.addMenu(menu)
    
  def mainMenuChoice(self, choice):
    """Prepares all the things for the main menu choice."""
    if choice:
      self.prepareWorld()
    self.done = True
      
  def prepareWorld(self):
    """Creates a world"""
    village = Village()
    village.generateWorld()
    self._nextState = ExploringState(village)
  
  def processEvent(self, gameEvent):
    """Bogus"""
    return
    

    
    
class ExploringState(GameState):
  """This game state represents being able to explore a world given to it."""
  def __init__(self, world):
    GameState.__init__(self)
    self._world = world

  def initialise(self):
    """Initialises menus, etc"""
    GameState.initialise(self)
    gameMap = GameMap(Display.MapX, Display.MapY, Display.MapW, Display.MapH,
                  "The Valley of the Wind", self._world, self._world.hero)
    # Add the map as as a purely graphical element
    self.addMenu(gameMap, False)
    
    charDisplay = CharDisplay(Display.MapW, 0, Display.RIGHT_MENU_SIZE, 200,
                  "Nausicaa's equipment", self._world.hero)
    # Add the char display as as a purely graphical element
    self.addMenu(charDisplay, False)
  
  def initMenus(self):
    """Initialise the regular menus, but also create the message menu"""
    GameState.initMenus(self)
    self.createMessageMenu()
    
  def createMessageMenu(self):
    self._messageHistory = TextBox(0, Display.MapH, Display.MapW, Display.BOTTOM_MENU_SIZE,
                                   "Message History")
    self.addMenu(self._messageHistory)
  
  
  def processEvent(self, gameEvent):
    """The input listener method that processes inputs."""
    
    # dt = -1 # TODO implement this!
    
    if Events.MOVE_UP in gameEvent.events:
      self.heroMove( 0, -1)
    elif Events.MOVE_UP_LEFT in gameEvent.events:
      self.heroMove(-1, -1)
    elif Events.MOVE_UP_RIGHT in gameEvent.events:
      self.heroMove( 1, -1)
    elif Events.MOVE_LEFT in gameEvent.events:
      self.heroMove(-1,  0)
    elif Events.MOVE_RIGHT in gameEvent.events:
      self.heroMove( 1,  0)
    elif Events.MOVE_DOWN in gameEvent.events:
      self.heroMove( 0,  1)
    elif Events.MOVE_DOWN_LEFT in gameEvent.events:
      self.heroMove(-1,  1)
    elif Events.MOVE_DOWN_RIGHT in gameEvent.events:
      self.heroMove( 1,  1)
    elif Events.PICKUP in gameEvent.events:
      self.addPickupMenu()
    elif Events.DROP in gameEvent.events:
      self.addDropMenu()
    elif Events.OPEN in gameEvent.events:
      self.openAction(True)
    elif Events.CLOSE in gameEvent.events:
      self.openAction(False)
    elif Events.EQUIPMENT in gameEvent.events:
      self.equipmentScreen()
    elif Events.EXIT in gameEvent.events:
      self.quitMenu()
  
  ############
  ### GAME ###
  ############
  
  def addMessage(self, text):
    """Add a message to the message history menu."""
    self._messageHistory.addMessage(text)
  
  def heroMove(self, dx, dy):
    """Moves the hero and advances the world by the required amount."""
    dt = self._world.hero.step(dx, dy)
    self._world.run(dt)
  
  def heroPickup(self, menu, items):
    """Makes the hero pick the items up."""
    self.removeMenu(menu)
    dt = self._world.hero.pickup(items)
    self._world.run(dt)
  
  def addPickupMenu(self):
    """Responds to pick up action. Creates a menu with items and waits for that
    input and sets its callback."""
    items = self._world.hero.parent.getPickableItems()
    menu = ListSelector(Display.MapW, 0,
                        Display.RIGHT_MENU_SIZE, 200,
                        "Pick up which items?",
                        [item.bp.name for item in items], items)
    menu.setCallback(self.heroPickup, [menu])
    self.addMenu(menu)
    
  def heroDrop(self, menu, items):
    """Makes the hero pick the items up."""
    self.removeMenu(menu)
    dt = self._world.hero.drop(items)
    self._world.run(dt)
  
  def addDropMenu(self):
    """Responds to pick up action. Creates a menu with items and waits for that
    input and sets its callback."""
    hero = self._world.hero
    values = list(hero.contents.keys())
    items = [item.bp.name for item in values]
    # Checks whether items are equipped and changes their names
    for i in range(len(items)):
      equippedAt = hero.isEquipped(values[i])
      if equippedAt != None:
        items[i] = items[i] + " [" + equippedAt.bp.name + "]"
        
    
    menu = ListSelector(Display.MapW, 0,
                        Display.RIGHT_MENU_SIZE, 200,
                        "Drop which items?",
                        items, values)
    menu.setCallback(self.heroDrop, [menu])
    self.addMenu(menu)
  
  def heroOpen(self, items):
    """The hero heroically opens something."""
    if len(items) > 0:
      self._world.hero.open(items[0])
  
  def heroClose(self, items):
    """The hero heroically closes something."""
    if len(items) > 0:
      self._world.hero.close(items[0])
  
  def openAction(self, isOpen):
    """First, requests a direction in which to open/close things. Should then
    open a menu will all openable things in that area, and will get to choose one."""
    if isOpen:
      text = "Open in what direction?"
    else:
      text = "Close in what direction?"
    
    menu = DirectionSelector(Display.MapW, 0,
                        Display.RIGHT_MENU_SIZE, 200,
                        "Direction selection", text)
    menu.setCallback(self.openWithDirection, [menu, isOpen])
    self.addMenu(menu)
  
  def openWithDirection(self, menu, isOpen, direction):
    """With the given direction, open/close a ListSingleSelector to choose what 
    item to open."""
    self.removeMenu(menu)
    if direction == None:
      return
    (heroX, heroY) = self._world.hero.getPos()
    openTile = self._world.getTile(heroX + direction[0], heroY + direction[1])
    
    if isOpen:
      items = openTile.getOpenableItems()
      text = "Open what?"
      function = self.heroOpen
    else:
      items = openTile.getClosableItems()
      text = "Close what?"
      function = self.heroClose
    
    if len(items) == 1:
      function(items)
    elif len(items) > 1:
      menu = ListSingleSelector(Display.MapW, 0,
                        Display.RIGHT_MENU_SIZE, 200,
                          text, [item.bp.name for item in items], items)
      menu.setCallback(function, [])
      self.addMenu(menu)
    else:
      menu = Dialog((Display.MapW - Display.RIGHT_MENU_SIZE) // 2,
                          Display.MapH // 2 - 50,
                          Display.RIGHT_MENU_SIZE, 100,
                          "Oops!", "There's nothing to open/close here")
      self.addMenu(menu)
      menu.setCallback(self.removeMenu, [menu])
  
  
  def equipmentScreen(self):
    """Opens up an equipment screen."""
    w = 600
    h = 400
    x = Display.MapX + Display.MapW // 2 - w // 2
    y = Display.MapY + Display.MapH // 2 - h // 2
    menu = EquipmentScreen(x, y, w, h, self._world.hero)
    self.addMenu(menu)
    menu.setCallback(self.equip, [menu])
  
  def equip(self, menu, equip, part, item):
    """Equip is a boolean saying whether the operation was cancelled or not.
    Part and item are the item you want to equip in the given part."""
    self.removeMenu(menu)
    # If the menu was cancelled, fogedaboudit    
    if not equip:
      return
    
    if item == None: # No item selected means unequip
      #got in here
      print("here")
      self._world.hero.unequip(part)
    else:
      self._world.hero.equip(part, item)
    
  
  
  def quitMenu(self):
    """Opens up a menu that asks whether the user wants to quit or not."""
    menu = ListSingleSelector((Display.MapW - Display.RIGHT_MENU_SIZE//2) // 2,
                          Display.MapH // 2 - 50,
                          Display.RIGHT_MENU_SIZE//2, 100,
                              "Really exit?",
                              ["Exit", "Cancel"], [True, False])
    menu.setCallback(self.quitExplore, [menu])
    self.addMenu(menu)
    
  def quitExplore(self, menu, isQuit=[False]):
    """Receives a singleton list with either True or False and possibly forces
    the game to exit this state."""
    self.removeMenu(menu)
    if len(isQuit) == 0:
      isQuit.append(False)
    if isQuit[0]:
      self.done = True
      self._nextState = TitleScreenState()

  def nextState(self):
    """Returns the next state."""
    return self._nextState
    
    
  def update(self, dt):
    """Meant to update the world according to real-time. Here used for world."""
    # print(dt) # fps counter ish
    for row in self._world.smap:
      for tile in row:
        tile.update(dt)
    
    
    
    
    
    
    
    
    
    
    
    