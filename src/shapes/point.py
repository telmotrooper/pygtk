# pylint: disable=no-name-in-module, import-error
from utils.gen_random_id import generateRandomId

class Point:
  def __init__(self, name):
    self.world_coords = []
    self.normalized_coords = []
    self.name = name
    self.id = generateRandomId()
  
  def addCoords(self, x, y):
    self.world_coords.append(
      {"x": x, "y": y}
    )
    self.normalized_coords.append(
      {"x": x, "y": y}
    )

  def getWorldCoords(self):
    return self.world_coords

  def getNormalizedCoords(self):
    return self.normalized_coords

  def getName(self):
    return self.name

  def getId(self):
    return self.id

  def draw(self, ctx, coords):  # Reference: https://pycairo.readthedocs.io/    
    x = coords[0]["xViewPort"]
    y = coords[0]["yViewPort"]
  
    ctx.move_to(x,y)
    ctx.rel_line_to(1,1)  # equivalent to ctx.line_to(x+1,y+1)
    ctx.stroke()

  def drawToViewport(self, ctx, viewport):   
    x, y = self.world_coords[0]["x"], self.world_coords[0]["y"]

    point = viewport.transform(x, y)
  
    ctx.move_to(point["x"],point["y"])
    ctx.rel_line_to(1,1)  # equivalent to ctx.line_to(x+1,y+1)
    ctx.stroke()
