import sfml


class ResourceManager:

  # Stores all images using an identifier
  _textures = {}
  
  @staticmethod
  def preload(sourcefile):
    """Preloads sourcefile so it's ready before it's asked for."""
    if not sourcefile in ResourceManager._textures:
      image = sfml.Texture.from_file(sourcefile)
      ResourceManager._textures[sourcefile] = image
  
  
  @staticmethod
  def getTexture(sourcefile):
    """Gets the spritesheet in ready-to-use format!"""
    ResourceManager.preload(sourcefile)
    
    return ResourceManager._textures[sourcefile]
  