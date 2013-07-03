from collections import deque

from nEngine.graphics.Display import Display
from nEngine.Input import *
from nEngine.Utility import Utility

""""GUI stuff!"""

def InitGUI():
  Frame.init()
  ListSelector.init()
  CharDisplay.init()
  ScrollTitleSelector.init()

  
class Sprite:
  """A sprite class that can be used as a menu to draw simple sprites/images."""
  
  def __init__(self, surface, pos, area=None):
    """Needs the filename, position, and possibly area of original image to draw."""
    
    # Location and size
    self._pos = pos
    self._area = area
    
    # The title of this screen
    self._sprite = surface
    
  def draw(self):
    Display.draw(self._sprite, self._pos, self._area)


class Frame:
  """A class that draws a frame with title (or not)"""
  
  @staticmethod
  def init():
    """Initialises border related data."""
    # Space necessary for horizontal and vertical borders
    Frame.BORDER_WIDTH = Display.TEXT_HEIGHT
    Frame.BORDER_HEIGHT = Display.TEXT_HEIGHT
  
  def __init__(self, x, y, w, h, title="???", background=True, border=True):
    """Needs position, size and title."""
    
    # Location and size
    self._x = x
    self._y = y
    self._w = w
    self._h = h
    
    # Starts unfocussed by default. Focussing makes the frame whiter.
    self.setFocus(False)
    
    # The title of this screen
    self._title = title
    
    self._border = border
    self._background = background
    
    # Render all the surfaces needed
    self.prepSurfaces()
    
    self.prepDrawData()
    
  
  def prepSurfaces(self):
    """Renders the title surface"""
    if self._border:
      self._titleSurface = Display.renderText(self._title, colour=(122,122,122))
      self._titleSurfaceFocus = Display.renderText(self._title, colour=(255,255,255))
    if self._background:
      self._backgroundSurface = Display.generateBackground((self._w, self._h), (0, 0, 0))
  
  
  def prepDrawData(self):
    """Prepares variables that indicate how to draw border, etc."""
    if not self._border:
      return
    self._TopLeft = (self._x + Frame.BORDER_WIDTH // 2,
                    self._y + Frame.BORDER_HEIGHT // 2)
    self._TopRight = (self._x + self._w - Frame.BORDER_WIDTH // 2,
                     self._y + Frame.BORDER_HEIGHT // 2)
    self._BottomLeft = (self._x + Frame.BORDER_WIDTH // 2,
                       self._y + self._h - Frame.BORDER_HEIGHT // 2)
    self._BottomRight = (self._x + self._w - Frame.BORDER_WIDTH // 2,
                        self._y + self._h - Frame.BORDER_HEIGHT // 2)
    self._TitleLeft = (self._x + Frame.BORDER_WIDTH // 2 + Display.TEXT_WIDTH,
                      self._y + Frame.BORDER_HEIGHT// 2)
    self._TitleRight = (self._x + Frame.BORDER_WIDTH // 2 +
                        2*Display.TEXT_WIDTH + self._titleSurface.get_width(),
                      self._y + Frame.BORDER_HEIGHT // 2)
  
  def draw(self):
    # Draw background
    if self._background:
      Display.draw(self._backgroundSurface, (self._x, self._y))
    # Draw border and title
    if self._border:
      if self._inFocus:
        colour = (255,255,255)
        titleSurface = self._titleSurfaceFocus
      else:
        colour = (122,122,122)
        titleSurface = self._titleSurface
      Display.drawLine(colour, self._TopLeft, self._TitleLeft)
      Display.drawLine(colour, self._TitleRight, self._TopRight)
      Display.drawLine(colour, self._TopRight, self._BottomRight)
      Display.drawLine(colour, self._BottomRight, self._BottomLeft)
      Display.drawLine(colour, self._BottomLeft, self._TopLeft)
      Display.draw(titleSurface, (self._x + ListSelector.BORDER_WIDTH + Display.TEXT_WIDTH, self._y))
  
  def drawPos(self):
    """Returns position for interior draw space."""
    if self._border:
      return (self._x + Frame.BORDER_WIDTH, self._y + Frame.BORDER_HEIGHT)
    else:
      return (self._x, self._y)

  def availableSpace(self):
    """Returns size of interior draw space."""
    if self._border:
      return (self._w - 2*Frame.BORDER_WIDTH, self._h - 2*Frame.BORDER_HEIGHT)
    else:
      return (self._w, self._h)
    
    
  def setCallback(self, callbackFun, args):
    """Sets what function will be called once this Frame/menu is ACCEPTed,
    and with what initial arguments."""
    self._callbackFun = callbackFun
    self._args = args
  
  def processCallback(self):
    """Execute the callback."""
    self._callbackFun(*self._args)
  
  def processEvent(self, gameEvent):
    """By default, GUI elements do not consume input."""
    return
    
  def setFocus(self, focus):
    """Sets whether this frame is in focus or not. If it is, the frames are
    drawn whiter."""
    self._inFocus = focus
    
    
    
class GameMap(Frame):
  """A GUI element that shows the world, focused on the some entity."""
  
  def __init__(self, x, y, w, h, title, world, actor, background=True, border=True):
    Frame.__init__(self, x, y, w, h, title)
    
    self._world = world
    
    self.setCenterActor(actor)
    
    self.repositionCameraOnFocus()
    
  def setCenterActor(self, actor):
    """Sets focus on some map entity (or, really, anything you can call getPos on."""
    self._center = actor
  
  def draw(self):
    """Draws the entire model on the screen."""
    # Draw the frame
    Frame.draw(self)
    
    # Set the camera in the right place
    self.repositionCameraOnFocus()
    
    redraw = []
    for row in self._world.smap:
      for tile in row:
        toRedraw = self.drawTile(tile)
        redraw.extend(toRedraw)
    
    for entity in redraw:
      self.drawEntity(entity, entity.getMainTile())
        
  
  def drawTile(self, tile):
    """Draws a single tile on the screen. Uses a breadth-first listing of the
    entity tree and only draws visible entities. Returns the set of entities to
    redraw."""
    
    toRedraw = []
    
    entities = tile.getVisibleItems()
    for entity in entities:
      # Only draw entities once, in their "main tile".
      if not entity.isMainTile(tile):
        continue
      
      # If it's a multi-tile display currently, just ask it to redraw later.
      if entity.display.isMultiTile():
        toRedraw.append(entity)
      else:
        self.drawEntity(entity, tile)
      
    
    return toRedraw
  
  def drawEntity(self, entity, tile):
    """Draws a single entity on screen, also given its main tile."""
    # GameMap draw position
    (drawX, drawY) = self.drawPos()
    
    # Frame and offset information
    frame = entity.display.frame
    (dx, dy) = entity.display.getOffset()
    (spriteW, spriteH) = frame.w, frame.h
    
    # Visible map tile on which the frame should be drawn
    tileX = tile.x - self.CAM_POS_X + dx
    tileY = tile.y - self.CAM_POS_Y + dy
    
    # Spritesheet coordinates for drawing
    spriteX = frame.x
    spriteY = frame.y
    
    # If the drawing would go outside the screen, adjust it
    # Adjust left limit
    if tileX < 0:
      diff = 0 - tileX
      spriteX = spriteX + diff
      spriteW = spriteW - diff
      tileX = 0
      if spriteW < 1:
        return
    
    # Adjust top limit
    if tileY < 0:
      diff = 0 - tileY
      spriteY = spriteY + diff
      spriteH = spriteH - diff
      tileY = 0
      if spriteH < 1:
        return
    
    # Adjust right limit
    # Aware of the -1 on both sides, I'm just using indices :)
    if tileX + spriteW - 1 > Display.DISPLAY_TILES_X - 1:
      diff = tileX + spriteW - (Display.DISPLAY_TILES_X)
      spriteW = spriteW - diff
      if spriteW < 1:
        return
    
    # Adjust right limit
    # Aware of the -1 on both sides, I'm just using indices :)
    if tileY + spriteH - 1 > Display.DISPLAY_TILES_Y - 1:
      diff = tileY + spriteH - (Display.DISPLAY_TILES_Y)
      spriteH = spriteH - diff
      if spriteH < 1:
        return
    
    Display.draw(entity.display.getSpritesheet(),
                           (tileX*Display.TILE_WIDTH + drawX,
                            tileY*Display.TILE_HEIGHT + drawY),
                           (spriteX*Display.TILE_WIDTH,
                            spriteY*Display.TILE_HEIGHT,
                            spriteW*Display.TILE_WIDTH,
                            spriteH*Display.TILE_HEIGHT))
  
  def repositionCameraOnFocus(self):
    """Looks at where the hero is and repositions the camera so he is near
    the center."""
    pos = self._center.getPos()
    self.repositionCamera(pos[0] - Display.DISPLAY_TILES_X // 2,
                          pos[1] - Display.DISPLAY_TILES_Y // 2)
  
  def repositionCamera(self, x, y):
    """Repositions the camera with x, y near the center. Will take care that
    the viewing limits are not exceeded."""
    
    self.CAM_POS_X = x
    self.CAM_POS_Y = y
    
    if self.CAM_POS_X < 0:
      self.CAM_POS_X = 0
    elif self.CAM_POS_X > self._world.WORLD_WIDTH - Display.DISPLAY_TILES_X:
      self.CAM_POS_X = self._world.WORLD_WIDTH - Display.DISPLAY_TILES_X
    
    if self.CAM_POS_Y < 0:
      self.CAM_POS_Y = 0
    elif self.CAM_POS_Y > self._world.WORLD_HEIGHT  - Display.DISPLAY_TILES_Y:
      self.CAM_POS_Y = self._world.WORLD_HEIGHT - Display.DISPLAY_TILES_Y
    

    
class CharDisplay(Frame):
  """Displays a character's information: his body parts, what he has equipped,
  etc."""
  
  @staticmethod
  def init():
    """Sets up a single text image."""
    CharDisplay._nothingSurface = Display.renderText("Nothing", colour=(122,122,122))
  
  def __init__(self, x, y, w, h, title, actor, background=True, border=True):
    self._actor = actor
    # Keep a local copy of items last shown
    self._equippedNames = []
    for part in self._actor._parts:
      if part.equipped == None:
        self._equippedNames.append(None)
      else:
        self._equippedNames.append(part.bp.name)
    
    # This calls self.prepDrawSurfaces!
    Frame.__init__(self, x, y, w, h, title, background=True, border=True)
    
  def prepSurfaces(self):
    """Renders all the text related to the actor's bodyparts."""
    Frame.prepSurfaces(self)
    
    # Stores surfaces for body parts
    self._partSurfaces = []
    
    for part in self._actor._parts:
      # Render bodypart text
      surface = Display.renderText(part.bp.name, colour=(122,122,122))
      self._partSurfaces.append(surface)
    
    # Set HP draw distance
    self._hpDrawX = max([s.get_width() for s in self._partSurfaces]) + 3*Display.TEXT_WIDTH
    
    # Stores surfaces for equipped item names
    self._equippedSurfaces = {}
    self.updateEquippedItems()
  
  def updateEquippedItems(self):
    """Checks whether the equipment used by the actor changed since last frame,
    and updates surfaces accordingly."""
    for i in range(len(self._actor._parts)):
      # Check all of the actor's currently equiped items
      # and for each that changed last frame, draw new surface
      item = self._actor._parts[i].equipped
      if item == None:
        self._equippedSurfaces[i] = CharDisplay._nothingSurface
        self._equippedNames[i] = "None"
      elif item.bp.name != self._equippedNames[i]:
        surface = Display.renderText(item.bp.name, colour=(122,122,122))
        self._equippedSurfaces[i] = surface
        self._equippedNames[i] = item.bp.name
  
  def draw(self):
    """Draws the character display."""
    # Draw the frame
    Frame.draw(self)
    
    # Check whether equipment has changed
    self.updateEquippedItems()
    
    # To start drawing, allocate space for the top border
    # drawY will keep track of the place to draw the items at
    (drawX, drawY) = self.drawPos()
    (drawW, _) = self.availableSpace()
    
    # Iterate all parts
    for i in range(len(self._actor._parts)):
      # Draw part names
      Display.draw(self._partSurfaces[i], (drawX, drawY))
      # Draw item
      itemSurface = self._equippedSurfaces[i]
      Display.draw(itemSurface, (drawX + drawW - itemSurface.get_width(), drawY))
      # Draw part HP
      hpStr = str(self._actor._parts[i].hp) + "/" + str(self._actor._parts[i].bp.hp)
      hpText = Display.renderText(hpStr, colour=(122,122,122))
      Display.draw(hpText, (drawX + self._hpDrawX, drawY))
      
      drawY = drawY + Display.TEXT_HEIGHT
    
    
    
    
    
class EquipmentScreen(Frame):
  """A menu to equip objects on different actor parts."""
  
  def __init__(self, x, y, w, h, actor, background=True, border=True):
    Frame.__init__(self, x, y, w, h, "Equipment", background, border)
    
    # Actor who is equipping things
    self._actor = actor
    
    # Set up some basic variables
    self.computePositions()
    
    # Set up left hand side list selector.
    values = self._actor._parts
    items = [i.bp.name for i in values]
    self._partsMenu = ListSingleSelector(self._partX, self._partY,
                                         self._partW, self._partH,
                                         "Body parts", items, values)
    self._partsMenu.select(0)
    self._partsMenu.setFocus(True)
    
    self.setupItemPartsMenu()
    
    self.setFocusOnParts(True)
  
  def computePositions(self):
    """Computes variables useful for positioning."""
    (drawX, drawY) = self.drawPos()
    (drawW, drawH) = self.availableSpace()
    
    self._partX = drawX + Display.TEXT_WIDTH
    self._partY = drawY + Display.TEXT_WIDTH
    self._partW = drawW / 2 - 2*Display.TEXT_WIDTH
    self._partH = drawH - 2*Display.TEXT_WIDTH
    self._itemX = drawX + drawW - drawW / 2
    self._itemY = drawY + Display.TEXT_WIDTH
    self._itemW = drawW / 2 - 2*Display.TEXT_WIDTH
    self._itemH = drawH - 2*Display.TEXT_WIDTH
  
  def setFocusOnParts(self, focus):
    """Sets whether the focus is on choosing parts or items."""
    self._partsFocus = focus
    if focus:
      self._partsMenu.setFocus(True)
      self._itemsMenu.setFocus(False)
    else:
      self._partsMenu.setFocus(False)
      self._itemsMenu.setFocus(True)
    
  
  def setupItemPartsMenu(self):
    """This checks which part is currently selected, then selects equippable
    items and shows them on secondary menu."""
    # Get part that is currently selected
    selectedPart = self._partsMenu.getSelectedItems()[0]
    
    # Create auxiliary arrays with items that can be equipped there.
    valuesAux = [item for item in self._actor.contents.keys() if selectedPart.canEquip(item)]
    itemsAux = [item.bp.name for item in valuesAux]
    # Check for equipped items to change their names.
    for i in range(len(itemsAux)):
      equippedAt = self._actor.isEquipped(valuesAux[i])
      if equippedAt != None:
        itemsAux[i] = itemsAux[i] + " [" + equippedAt.bp.name + "]"
    # Allow equiping nothing or removing equipment!
    items = ["Take off / Nothing"]
    values = [None]
    items.extend(itemsAux)
    values.extend(valuesAux)
    
    self._itemsMenu = ListSingleSelector(self._itemX, self._itemY,
                                         self._itemW, self._itemH,
                                         "Body parts", items, values)
  
  def populateArgs(self, accept):
    """Populates the callback function's arguments based on current items and
    whether the form was accepted or cancelled."""
    # Appends whether the form was cancelled or not.
    self._args.append(accept)
    # Adds chosen parts!
    part = self._partsMenu.getSelectedItems()[0]
    item = self._itemsMenu.getSelectedItems()
    if len(item) == 0: # If there is nothing selected as an item
      item = None
    else:
      item = item[0]
    self._args.append(part)
    self._args.append(item)
  
  def processEvent(self, gameEvent):
    """TODO TOTALLY NOT DONE"""
    # Consumes all events until a selection is made!
    # This includes movements and stuff.
    gameEvent.consumed = True

    # If it's a switch, then change to the other menu
    if (Events.SWITCH in gameEvent.events or
        Events.SELECT_LEFT in gameEvent.events or
        Events.SELECT_RIGHT in gameEvent.events):
      self.setFocusOnParts(not self._partsFocus)
      return
    
    # Does the user no longer want to do this?
    if Events.EXIT in gameEvent.events:
      self.populateArgs(False)
      self.processCallback()
      return
    
    # Is the choice made?
    if Events.ACCEPT in gameEvent.events:
      self.populateArgs(True)
      self.processCallback()
      return
    
    
    
    # If it's other regular input, pass it on to focussed selector
    if self._partsFocus:
      self._partsMenu.processEvent(gameEvent)
    else:
      self._itemsMenu.processEvent(gameEvent)
      
    # If it was a selection action for the first menu, then it is possible the
    # items menu should be updated
    event = Input.containsEventOfType(gameEvent, "SELECTION")
    relEvent = Input.containsEventOfType(gameEvent, "RELATIVE_SELECTION")
    if self._partsFocus and (event != None or relEvent != None):
      self.setupItemPartsMenu()
    
    
  def draw(self):
    """Draw itself, plus the other menus."""
    Frame.draw(self)
    self._partsMenu.draw()
    self._itemsMenu.draw()
    
    
    
class ListSelector(Frame):
  """A list of items from which you can choose multiple."""
  
  @staticmethod
  def init():
    """Initialises all generic surfaces required such as selector indices,
    scroll indicators and so forth."""
    
    # This sets how much space is taken up by the indicators
    ListSelector.INDICADOR_OFFSET = 25
  
    # Renders extra visual cues for whether items are selected.
    ListSelector.SelectedIndicators = []
    ListSelector.UnselectedIndicators = []
    for c in "abcdefghijklmnopqrstuvwxyz":
      indicator = Display.renderText("[%c] " % c, colour=(255,255,255))
      ListSelector.SelectedIndicators.append(indicator)
      indicator = Display.renderText("(%c) " % c, colour=(122,122,122))
      ListSelector.UnselectedIndicators.append(indicator)
    
    ListSelector.ScrollUpIcon = Display.renderText("----", colour=(122,122,122))
    ListSelector.ScrollDownIcon = Display.renderText("++++", colour=(122,122,122))
    
    
    
  def __init__(self, x, y, w, h, title, items, values, background=True, border=True):
    """Game is the base game, x and y are the coordinates at which the menu will
    be drawn, items is list of strings containing what is displayed, values is
    the list of values associated with each item, and the width and height are
    the dimensions the selector should have."""
    
    self.items = items # All the entities themselves
    self.values = values # All the values themselves
    
    # After extra data has been assigned, call superclass init, which should
    # call this class's prepDrawSurfaces method
    Frame.__init__(self, x, y, w, h, title, background, border)
    
    self.selected = [] # Contains indexes of selected entities
    
    self.firstIndex = 0
    
    # The maximum number of lines accounts for the top and bottom borders
    # which are 1 line height each.
    (w, h) = self.availableSpace()
    self.maxLines = h // Display.TEXT_HEIGHT
    
    # If there's not enough space to draw all the lines, it allocates some extra
    # space for the scrolling indicators
    
    if self.maxLines < len(items):
      self.maxLines = self.maxLines - 2
    
    # Updates list of indices of items to be drawn
    self.updateItemsToDraw()
  
  def _availableWidth(self):
    """Returns the width available with indicators."""
    (w, _) = self.availableSpace()
    return w - ListSelector.INDICADOR_OFFSET
  
  def prepSurfaces(self):
    """Renders all the text related to the items."""
    Frame.prepSurfaces(self)
    
    self.unselectedSurfaces = []
    self.selectedSurfaces = []
    
    for item in self.items:
      # First, limit text width.
      text = Display.limitText(item, self._availableWidth())
      
      # Render text for items when they are selected
      surface = Display.renderText(text, colour=(255,255,255))
      self.selectedSurfaces.append(surface)
      
      # Render text for items when they are unselected
      surface = Display.renderText(text, colour=(122,122,122))
      self.unselectedSurfaces.append(surface)
  
  def select(self, index):
    """Toggles the selection for item with given index."""
    trueIndex = index + self.firstIndex
    if trueIndex >= len(self.items):
      return
    if trueIndex in self.selected:
      self.selected.remove(trueIndex)
    else:
      self.selected.append(trueIndex)
  
  def lastVisibleIndex(self):
    """Returns the index of the last visible item on the list."""
    return self.firstIndex + self.maxLines
  
  def canScrollDown(self):
    """Determines whether it is possible to scroll down the list."""
    return self.lastVisibleIndex() < len(self.items) - 1
    
  def canScrollUp(self):
    """Determines whether it is possible to scroll up the list"""
    return self.firstIndex > 0
  
  def scrollable(self):
    """Returns whether this list can be scrolled (up or down)."""
    return self.canScrollDown() or self.canScrollUp()
  
  def scrollDown(self):
    """When there is insufficient space, shows next page."""
    self.firstIndex = self.firstIndex + self.maxLines
    if self.firstIndex >= len(self.items):
      self.firstIndex = len(self.items)-1
    
    self.updateItemsToDraw()
    
  def scrollUp(self):
    """When there is insufficient space, shows previous page."""
    self.firstIndex = self.firstIndex - self.maxLines
    if self.firstIndex < 0:
      self.firstIndex = 0
    
    self.updateItemsToDraw()
  
  def updateItemsToDraw(self):
    """Updates the indices of items to show (should be called after scrolling)."""
    allIndex = range(len(self.items))
    self.itemsToDraw = allIndex[self.firstIndex:(self.firstIndex+self.maxLines)]
  
  def drawScrollUp(self):
    """Draws scroll up indicador."""
    (drawX, drawY) = self.drawPos()
    (drawW, _) = self.availableSpace()
    posX = drawX + drawW - ListSelector.ScrollUpIcon.get_width()
    posY = drawY
    Display.draw(ListSelector.ScrollUpIcon, (posX, posY))
  
  def drawScrollDown(self):
    """Draws scroll down indicador."""
    (drawX, drawY) = self.drawPos()
    (drawW, drawH) = self.availableSpace()
    posX = drawX + drawW - ListSelector.ScrollUpIcon.get_width()
    posY = drawY + drawH - Display.TEXT_HEIGHT
    Display.draw(ListSelector.ScrollDownIcon, (posX, posY))
  
  def draw(self):
    """Draws the ListSelector at the x, y position."""
    
    # draw frame
    Frame.draw(self)
    
    # To start drawing, allocate space for the top border
    # drawY will keep track of the place to draw the items at
    (drawX, drawY) = self.drawPos()
    # If scrolling is a necessity, allocate space for top scroll indicator
    if self.scrollable():
      drawY = drawY + Display.TEXT_HEIGHT
      
      # and draw all the indicators (as appropriate)
      if self.canScrollUp():
        self.drawScrollUp()
      if self.canScrollDown():
        self.drawScrollDown()
    
    # Draw items
    indicator = 0
    for i in self.itemsToDraw:
      if i in self.selected:
        Display.draw(ListSelector.SelectedIndicators[indicator], (drawX, drawY))
        Display.draw(self.selectedSurfaces[i], (drawX + ListSelector.INDICADOR_OFFSET, drawY))
      else: 
        Display.draw(ListSelector.UnselectedIndicators[indicator], (drawX, drawY))
        Display.draw(self.unselectedSurfaces[i], (drawX + ListSelector.INDICADOR_OFFSET, drawY))
      
      drawY = drawY + Display.TEXT_HEIGHT
      indicator = indicator + 1
  
  def getSelectedItems(self):
    """Returns the list of entities selected in this list."""
    return [self.values[i] for i in self.selected]
    
  def processEvent(self, gameEvent):
    """The input listener method that processes inputs."""
    # Consumes all events until a selection is made!
    # This includes movements and stuff.
    gameEvent.consumed = True
    
    # Are we scrolling he menu up or down?
    if Events.SCROLL_UP in gameEvent.events:
      if self.canScrollUp(): self.scrollUp()
      return
    
    if Events.SCROLL_DOWN in gameEvent.events:
      if self.canScrollDown(): self.scrollDown()
      return
    
    # Does the user no longer want to do this?
    if Events.EXIT in gameEvent.events:
      self._args.append(list())
      self.processCallback()
      return
    
    # Is the choice made?
    if Events.ACCEPT in gameEvent.events:
      self._args.append(self.getSelectedItems())
      self.processCallback()
      return
    
    # Check whether there is a selection event
    event = Input.containsEventOfType(gameEvent, "SELECTION")
    if event != None:
      selectionIndex = Input.selectionToIndex(event)
      
      # If the selected index is actually visible, then select it!
      if selectionIndex < self.maxLines and selectionIndex < len(self.items):
        self.select(selectionIndex)
      
      # No need to do anything else.
      return 
   
    
class ListSingleSelector(ListSelector):
  """Same as ListSelector, but instead only allows one item to be selected
  at a time. Beware that getSelectedItems() returns a singleton list."""
  
  def __init__(self, x, y, w, h, title, items, values, background=True, border=True):
    ListSelector.__init__(self, x, y, w, h, title, items, values, background=True, border=True)
    if len(self.items) > 0:
      self.select(0)
  
  def select(self, index):
    self.selected = []
    ListSelector.select(self, index)
  
  def processEvent(self, gameEvent):
    """Besides the regular list, it allows users to move the selector up and
    down using the SCROLL_UP and SCROLL_DOWN commands."""
    
    ListSelector.processEvent(self, gameEvent)
    
    # Also, scrollllllll!
    if Events.SCROLL_UP in gameEvent.events or Events.SELECT_UP in gameEvent.events:
      self.moveUp()
      return
    
    if Events.SCROLL_DOWN in gameEvent.events or Events.SELECT_DOWN in gameEvent.events:
      self.moveDown()
      return
  
  def moveUp(self):
    """Moves the single selected item up"""
    # If there are no items, stop
    if len(self.items) == 0:
      return
      
    # If nothing is selected, select the first one available
    if len(self.selected) == 0:
      self.select(self.firstIndex)
      return
    
    # We know something is selected currently.
    selection = self.selected[0]
    if selection > self.firstIndex and selection > 0:
      self.selected[0] = selection - 1
    
  
  def moveDown(self):
    """Moves the single selected item down"""
    # If there are no items, stop
    if len(self.items) == 0:
      return
      
    # If nothing is selected, select the first one available
    if len(self.selected) == 0:
      self.select(self.firstIndex)
      return
    
    # We know something is selected currently.
    selection = self.selected[0]
    if selection < len(self.items)-1 and selection < self.firstIndex + self.maxLines:
      self.selected[0] = selection + 1
    
    
    
    
class TextBox(Frame):
  """A text box for... text!"""
    
  def __init__(self, x, y, w, h, title, background=True, border=True):
    """Game is the base game, x and y are the position of the menu, w and h are
    the dimensions, title is the title of the frame and bufferSize is the number
    of messages to keep."""
    
    # Call superclass init, which should
    # call this class's prepDrawSurfaces method
    Frame.__init__(self, x, y, w, h, title, background, border)
    
    # The text itself, works as a queue
    self._textSurfaces = deque()
    
    # The maximum number of lines accounts for the top and bottom borders
    # which are 1 line height each.
    (w, h) = self.availableSpace()
    self._maxLines = h // Display.TEXT_HEIGHT
    
  def addMessage(self, text):
    surfaces = Display.renderWrappedText(self._w, text, colour=(122,122,122))
    for surface in surfaces:
      if len(self._textSurfaces) == self._maxLines:
        self._textSurfaces.popleft()
      self._textSurfaces.append(surface)
      
  def draw(self):
    """Draws the textbox..."""
    # Draw frame first
    Frame.draw(self)
    
    # Get drawing positions
    (drawX, drawY) = self.drawPos()
    drawY = drawY + self._maxLines*Display.TEXT_HEIGHT
    for surface in self._textSurfaces:
      Display.draw(surface, (drawX, drawY))
      drawY = drawY - Display.TEXT_HEIGHT
  
  def processEvent(self, gameEvent):
    """Does not consume input"""
    return

    
    
    
    
class Dialog(Frame):
  """A simply dialog that shows a message."""
    
  def __init__(self, x, y, w, h, title, text):
    Frame.__init__(self, x, y, w, h, title)
    self.text = text
    self.questionSurface = Display.renderText(text, colour=(122,122,122))
    
  def draw(self):
    """Draws the textbox..."""
    # Draw frame first
    Frame.draw(self)
    
    # Get drawing positions
    (x, y) = self.drawPos()
    (w, h) = self.availableSpace()
    drawX = x + w // 2 - self.questionSurface.get_width() // 2
    drawY = y + h // 2 - self.questionSurface.get_height() // 2
    
    Display.draw(self.questionSurface, (drawX, drawY))
    
  
  def processEvent(self, gameEvent):
    """Consumes all input until an ACCEPT or EXIT event come along"""
    gameEvent.consumed = True
    # Exit selector?
    if Events.EXIT in gameEvent.events or Events.ACCEPT in gameEvent.events:
      self.processCallback()
      return
    
    
    
    
class DirectionSelector(Dialog):
  """Asks for user input for a direction."""
    
  def __init__(self, x, y, w, h, title, text):
    Dialog.__init__(self, x, y, w, h, title,  text)
  
  def processEvent(self, gameEvent):
    """The input listener method that processes inputs. Needs a callback!"""
    # All input is blocked until this selector is resolved.
    gameEvent.consumed = True
    
    # Exit selector?
    if Events.EXIT in gameEvent.events:
      self._args.append(None)
      self.processCallback()
      return
    
    # We don't want the hero to move until a choice has been made!
    event = Input.containsEventOfType(gameEvent, "MOVEMENT")
    if event != None:
      if event == Events.MOVE_CLIMB or event == Events.MOVE_DESCEND:
        return
      movPair = Utility.movementEventToVector(event)
      self._args.append(movPair)
      self.processCallback()
      



class ScrollTitleSelector(Frame):
  """A list of items with a selector that goes up and down"""
  
  @staticmethod
  def init():
    """Initialises all generic surfaces required such as selector indices,
    scroll indicators and so forth."""
    
    # This sets how much space is taken up by the indicators
    ScrollTitleSelector.INDICADOR_OFFSET = 60
  
    # Renders extra visual cues for whether items are selected.
    ScrollTitleSelector.indicator = Display.renderTitleText("(*) ", colour=(255,255,255))
    
    
  def __init__(self, x, y, w, h, title, items, values):
    """Game is the base game, x and y are the coordinates at which the menu will
    be drawn, items is list of strings containing what is displayed, values is
    the list of values associated with each item, and the width and height are
    the dimensions the selector should have."""
    
    self.items = items # All the entities themselves
    self.values = values # All the values themselves
    
    # After extra data has been assigned, call superclass init, which should
    # call this class's prepDrawSurfaces method
    Frame.__init__(self, x, y, w, h, title, False, False)
    
    self.selected = 0 # Contains indexes of the selected entry

  def prepSurfaces(self):
    """Renders all the text related to the items."""
    Frame.prepSurfaces(self)
    
    self.unselectedSurfaces = []
    self.selectedSurfaces = []
    
    for item in self.items:
      # Render text for items when they are selected
      surface = Display.renderTitleText(item, colour=(255,255,255))
      self.selectedSurfaces.append(surface)
      
      # Render text for items when they are unselected
      surface = Display.renderTitleText(item, colour=(255,255,255))
      self.unselectedSurfaces.append(surface)
  
  def moveDown(self):
    """When there is insufficient space, shows next page."""
    self.selected = self.selected + 1
    if self.selected == len(self.items):
      self.selected = 0
    
    
  def moveUp(self):
    """When there is insufficient space, shows previous page."""
    self.selected = self.selected - 1
    if self.selected == -1:
      self.selected = len(self.items) - 1
  
  def draw(self):
    """Draws the ListSelector at the x, y position."""
    
    # draw frame
    Frame.draw(self)
    
    # To start drawing, allocate space for the top border
    # drawY will keep track of the place to draw the items at
    (drawX, drawY) = self.drawPos()

    # Draw items
    for i in range(len(self.items)):
      if i == self.selected:
        Display.draw(ScrollTitleSelector.indicator, (drawX, drawY))
        Display.draw(self.selectedSurfaces[i], (drawX + ScrollTitleSelector.INDICADOR_OFFSET, drawY))
      else: 
        Display.draw(self.unselectedSurfaces[i], (drawX + ScrollTitleSelector.INDICADOR_OFFSET, drawY))
      
      (_, textHeight) = self.unselectedSurfaces[i].get_size()
      
      drawY = drawY + textHeight
  
  def getSelectedItems(self):
    """Returns the list of entities selected in this list."""
    return self.values[self.selected]
    
  def processEvent(self, gameEvent):
    """The input listener method that processes inputs."""
    # Consumes all events until a selection is made!
    # This includes movements and stuff.
    gameEvent.consumed = True
    
    # Are we scrolling he menu up or down?
    if Events.SCROLL_UP in gameEvent.events or Events.SELECT_UP in gameEvent.events:
      self.moveUp()
      return
    
    if Events.SCROLL_DOWN in gameEvent.events or Events.SELECT_DOWN in gameEvent.events:
      self.moveDown()
      return
    
    # Does the user no longer want to do this?
    if Events.EXIT in gameEvent.events:
      # Append that the user does not wish to exit the area
      self._args.append(None)
      self.processCallback()
      return
    
    # Is the choice made?
    if Events.ACCEPT in gameEvent.events:
      self._args.append(self.values[self.selected])
      self.processCallback()
      return
    


















