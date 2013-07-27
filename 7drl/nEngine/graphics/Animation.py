from sfml import Drawable, Transformable

class Frame:
  def __init__(self, rect, duration, centerpoint = None):
    self._rect = rect
    self._duration = duration
    self._centerpoint = centerpoint


class SpriteAnimation:
  def __init__(self, texture):
    self._texture = texture
    self._frames = []
  
  def addFrame(self, frame):
    self._frames.append(frame)
    
  def getTexture(self):
    return self._texture

  def getFrame(self, n):
    return self._frames[n]
  
  def getSize(self):
    return len(self._frames)



class AnimatedSprite(Drawable, Transformable):
  def __init__(self, animation):
    self._anim = animation
    self._frameNum
    self._timeInFrame = 0
    
    self.multiplier = 1.0
    self.loop = True
  
  def getFrameInfo(self):
    self._anim.getFrame(self._frameNum)
  
  def getFrameDuration(self):
    self.getFrameInfo[0]
  
  def getFrameRect(self):
    self.getFrameInfo[1]
  
  def toNextFrame(self):
    self._timeInFrame = self._timeInFrame - self.getFrameDuration()
    if self._frameNum < self._anim.getSize() - 1:
      self._frameNum = self._frameNum + 1
    else:
      if self.loop:
        self._frameNum = 0
      else:
        pass
  
  def run(self, dt):
    self._timeInFrame = self._timeInFrame + dt * self.multiplier
    while self._timeInFrame > self.getFrameDuration():
      self.toNextFrame()

