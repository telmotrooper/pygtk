from transform import Transform
from display_file import DisplayFile
import numpy as np

class Window:
  orientation = 0

  def __init__(self, x_min, y_min, x_max, y_max):
    Window.x_min = x_min
    Window.y_min = y_min
    Window.x_max = x_max
    Window.y_max = y_max
    Window.transformation = Transform()
    Window.display_file = DisplayFile()

  def getMin(self):
    return { "x": Window.x_min, "y": Window.y_min }

  def getMax(self):
    return { "x": Window.x_max, "y": Window.y_max }

  def getWidth(self):
    return Window.x_max - Window.x_min
  
  def getHeight(self):
    return Window.y_max - Window.y_min

  def getCenter(self):
    # print("window from ({},{}) to ({},{})".format(Window.x_min, Window.y_min, Window.x_max, Window.y_max))
    width, height = self.getWidth(), self.getHeight()

    center_x = (width / 2) + Window.x_min
    center_y = (height / 2) + Window.y_min

    # print("center at ({},{})".format(center_x, center_y))
    
    return {
      "x": center_x,
      "y": center_y
    }

  def zoom(self, percentage):
    center = self.getCenter()
    # print(self.getHeight())
    new_height = self.getHeight() * percentage
    new_width =  self.getWidth() * percentage
    # print("old height: {} new height: {}".format(self.getHeight(), new_height))
    
    new_x_min = center["x"] - (self.getWidth() / 2)
    new_x_max = center["x"] + (self.getWidth() / 2)

    new_y_min = center["y"] - (self.getHeight() / 2)
    new_y_max = center["y"] + (self.getHeight() / 2)

    self.setMin(new_x_min, new_y_min)
    self.setMax(new_x_max, new_y_max)

    for i in Window.display_file.getObjects():
      i.normalizeCoords()

  def setMin(self, x, y):
    Window.x_min = x
    Window.y_min = y
  
  def setMax(self, x, y):
    Window.x_max = x
    Window.y_max = y

  def move(self, x, y):
    Window.x_min += x
    Window.y_min += y
    Window.x_max += x
    Window.y_max += y

    for i in Window.display_file.getObjects():
      i.normalizeCoords()

    # print("Window at ({},{}) ({},{})".format(Window.x_min, Window.y_min, Window.x_max, Window.y_max))

  def rotate(self, direction, angle):
    if(direction == "left"):
      for i in self.display_file.getObjects():
        i.rotateNormalizedCoords(angle)
    else:
      for i in self.display_file.getObjects():
        i.rotateNormalizedCoords(-angle)
      

