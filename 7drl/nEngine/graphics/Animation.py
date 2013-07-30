from sfml import Drawable, Transformable, Rectangle

import nEngine.graphics.ResourceManager

class Frame:
  def __init__(self, rect = None, duration = None, centerpoint = None):
    self._rect = rect
    self._duration = duration
    self._centerpoint = centerpoint
    
  def loadFromXML(self, XMLRoot):
    split = XMLRoot.text.split(",")
    self._duration = float(split[-1])
    split = [int(p) for p in split[:-1]]
    self._rect = Rectangle((split[0], split[1]), (split[2], split[3]))
    self._centerpoint = (split[0], split[1])
    


class SpriteAnimation:
  def __init__(self, texture = None, frames = [], name = "SpriteAnimation"):
    self._texture = texture
    self._frames = frames
    self._name = name
  
  def loadFromXML(self, XMLRoot):
    self._name = XMLRoot.attributes["name"]
    self._texture = nEngine.graphics.ResourceManager.ResourceManager.getTexture(XMLRoot.attributes["name"])
    for frameRoot in XMLRoot:
      frame = Frame()
      frame.loadFromXML(frameRoot)
      self._frames.append(frame)
  
  def addFrame(self, frame):
    self._frames.append(frame)
    
  def getTexture(self):
    return self._texture

  def getFrame(self, n):
    return self._frames[n]
  
  def getSize(self):
    return len(self._frames)



class AnimatedSprite:
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

