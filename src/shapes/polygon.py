class Polygon:
  def __init__(self, name):
    self.coords = []
    self.name = name
  
  def addCoords(self, x, y):
    self.coords.append(
      {"x": x, "y": y}
    )

  def getCoords(self):
    return self.coords

  def getName(self):
    return self.name

  def draw(self, ctx, coords):  # reference: https://pycairo.readthedocs.io/
    ctx.move_to(coords[0]["xViewPort"], coords[0]["yViewPort"])

    for entry in coords:  # 1st interation does move_to and line_to to same point
      x2 = entry["xViewPort"]
      y2 = entry["yViewPort"]
      ctx.line_to(x2,y2)
    ctx.close_path()
    ctx.stroke()

  def drawToViewport(self, ctx, viewport):
    point = viewport.transform(self.coords[0]["x"], self.coords[0]["y"])
    ctx.move_to(point["x"],point["y"])

    for entry in self.coords:  # 1st interation does move_to and line_to to same point
      x2, y2 = entry["x"], entry["y"]
      point2 = viewport.transform(x2, y2)
      ctx.line_to(point2["x"],point2["y"])
    ctx.close_path()
    ctx.stroke()
