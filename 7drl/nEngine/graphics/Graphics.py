from nEngine.Rand import Rand

class Frame:
  """This class maintains all information pertaining to a single drawn frame of
  an animation. Contains the position and space """
  def __init__(self, x, y, w, h, duration):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.duration = duration


class Animation:
  """This class contains an animation's information. It does not run or maintain
  information about a currently running animation. Data members:
  - name: the animation's name.
  - spritesheet: the SDL surface that's going to be drawn from
  - random: boolean stating if the starting frame in the animation is random
  - repeat: boolean stating whether the animation repeats
  - nextAnimation: string identifying the animation to start after the current one ends
  - frames: list of frames to draw
  - dx, dy: distance from the bottom-left of the object's position to the
            top-left of the sprite to draw
  """
  
  def __init__(self, name, spritesheet, random, repeat, nextAnimation, frames, dx = 0, dy = 0):
    self.name = name
    self._spritesheet = spritesheet
    self.random = random
    self.repeat = repeat
    self.nextAnimation = nextAnimation
    self.frames = frames
    self._dx = dx
    self._dy = dy
    
    self.compute()
    
  def compute(self):
    """Computes a times list containing accumulated times for the animation, and
    a final time variable that's useful to determine when to change to the next
    animation."""
    self.times = []
    timer = 0
    for frame in self.frames:
      timer = timer + frame.duration
      self.times.append(timer)
    self.finalTime = self.times[-1]
  
  def getFrameByIndex(self, index):
    """Returns frame given by the index."""
    return self.frames[index]
  
  def getFrame(self, time):
    """Returns the frame associated with the current time. It is expected that
    the time is within the time bounds of the animation."""
    if time > self.finalTime:
      print("[ERROR] Getting frame for out-of-bounds time.")
      return None
    
    index = 0
    while time > self.times[index]:
      index = index + 1
    
    return self.frames[index]
  
  def getRandomFrame(self):
    """Returns a random frame in the current animation. This is useful for the
    entities that have multiple alternative graphics."""
    
    return self.frames[Rand.r.randint(0, len(self.frames)-1)]
    
    
  def isStill(self):
    """Returns whether this animation is made of stills or not."""
    return self.finalTime < 0
    
    
class DisplayBlueprint:
  """All the display information pertaining to one entity."""
  def __init__(self, default, animations):
    self.defaultAnimationName = default
    self.animations = {}
    for animation in animations:
      self.animations[animation.name] = animation

  def getAnimation(self, name):
    """Returns the animation given by the parameter."""
    return self.animations[name]
  
  def construct(self):
    """Returns a display with this blueprint."""
    return Display(self)
    
    
    
    
class Display:
  """Class that maintains the information about the current display status of
  each entity."""
  
  def __init__(self, displayBlueprint):
    self._dbp = displayBlueprint
    self.startAnimation(self._dbp.defaultAnimationName)
    self.time = 0

    if self._animation.random:
      if self._animation.isStill(): # If it's a still, choose frame by index
        self.frame = self._animation.getRandomFrame()
      else: # If it's not a still, choose it by time.
        self.time = Rand.r.randint(0, self._animation.finalTime-1)
    
  
  def startAnimation(self, animationName, time = 0):
    """Starts playing a new animation with the given name, and starting at time
    0 by default. Animations that repeat can start a little bit later."""
    self._animation = self._dbp.getAnimation(animationName)
    if self._animation.isStill():
      self.frame = self._animation.getFrameByIndex(0)
    else: # It's a dynamic thing, so set the time and go!
      self.time = time
      self.computeCurrentFrame()
  
  def finishAnimation(self):
    """Stops current animation and if it repeats, restart it. If it does not,
    starts next animation."""
    dt = (self.time - self._animation.finalTime)
    if dt < 0:
      dt = 0
    if self._animation.repeat:
      # The mod operation is there to account for large dt's wrapping around the
      # entire animation.
      self.startAnimation(self._animation.name, dt % self._animation.finalTime)
    else:
      self.startAnimation(self._animation.nextAnimation)
    
    self.computeCurrentFrame()
  
  def update(self, dt):
    """Updates animation status."""
    # If this is a static frame, do nooothinnnngggg
    if self.frame.duration == -1:
      return
    
    self.time = self.time + dt
    if self.time > self._animation.finalTime:
      self.finishAnimation()
    else:
      self.computeCurrentFrame()
  
  def computeCurrentFrame(self):
    """Computes the current frame."""
    self.frame = self._animation.getFrame(self.time)
    
  def getSpritesheet(self):
    """Returns the spritesheet from which the current frame will be drawn."""
    return self._animation._spritesheet
  
  def getOffset(self):
    """Returns the drawing offset."""
    return (self._animation._dx, self._animation._dy)
  
  def isMultiTile(self):
    """Returns whether this entity is currently multi-tiled."""
    return self.frame.w > 1 or self.frame.h > 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    