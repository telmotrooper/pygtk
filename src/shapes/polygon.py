import numpy as np
# pylint: disable=no-name-in-module, import-error
from utils.gen_random_id import generateRandomId
from transform import Transform
class Polygon:
  def __init__(self, name):
    self.world_coords = []
    self.normalized_coords = []
    self.name = name
    self.id = generateRandomId()
    self.transform = Transform()
  
  def addCoords(self, x, y):
    self.world_coords.append(
      {"x": x, "y": y}
    )
    self.normalized_coords.append(self.transform.normalize(x, y))

  def getWorldCoords(self):
    return self.world_coords

  def getNormalizedCoords(self):
    return self.normalized_coords
  
  def rotateNormalizedCoords(self, angle):
    angle_rad = np.deg2rad(angle)
    for i in range(len(self.normalized_coords)):
      coords = self.normalized_coords[i]
      print(coords)

      x = coords["x"] * np.cos(angle_rad) - coords["y"] * np.sin(angle_rad)
      y = coords["x"] * np.sin(angle_rad) - coords["y"] * np.cos(angle_rad)

      self.normalized_coords[i] = { "x": x, "y": y}
      print(self.normalized_coords[i])

  def setWorldCoords(self, i, x, y):
    self.world_coords[i] = { "x": x, "y": y }
    self.normalized_coords[i] = self.transform.normalize(x, y)

  def normalizeCoords(self):
    for i in range(len(self.world_coords)):
      x, y = self.world_coords[i]["x"], self.world_coords[i]["y"]
      self.normalized_coords[i] = self.transform.normalize(x, y)

  def getName(self):
    return self.name

  def getId(self):
    return self.id

  def drawToViewport(self, ctx, viewport):
    # move context to initial point
    point = viewport.transform(self.normalized_coords[0]["x"], self.normalized_coords[0]["y"])
    ctx.move_to(point["x"],point["y"])

    for entry in self.normalized_coords:  # 1st interation does move_to and line_to to same point
      x2, y2 = entry["x"], entry["y"]
      point2 = viewport.transform(x2, y2)
      ctx.line_to(point2["x"],point2["y"])
    ctx.close_path()
    ctx.stroke()
