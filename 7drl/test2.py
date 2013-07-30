from nEngine.Entities import EntityFactory
from nEngine.Entities import World


w = World()
f = EntityFactory.getSingleton()
f.readFile("planet5521/data/entities.xml")
f.produce(w, "XCC Grunt")
for key in f._map:
  f.produce(w, key)