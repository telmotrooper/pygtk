import numpy as np
from display_file import DisplayFile
from matrices import Matrices
from variables import clipping_border_size as cbz

display_file = DisplayFile()

class Transform:
  a,b = -1, 1

  def __init__(self):
    self.m = Matrices()

  def setWindow(self, window):
    Transform.window = window

  def normalize(self, x, y):
    # x' = (b-a) * ((x - min) / (max - min)) + a
    window = Transform.window
    a,b = self.a, self.b
    wmin_x, wmax_x = window.getMin()["x"] + cbz, window.getMax()["x"] - cbz
    wmin_y, wmax_y = window.getMin()["y"] + cbz, window.getMax()["y"] - cbz

    # print("(Transform) Window at ({},{}) ({},{})".format(wmin_x, wmin_y, wmax_x, wmax_y))

    new_x = (b-a) * ((x - wmin_x) / (wmax_x - wmin_x)) + a
    new_y = (b-a) * ((y - wmin_y) / (wmax_y - wmin_y)) + a

    return {"x": new_x, "y": new_y}

  def denormalize(self, x, y):
    # x' = (b-a) * ((x - min) / (max - min)) + a
    window = Transform.window
    a_x, b_x = window.getMin()["x"] + cbz, window.getMax()["x"] - cbz
    a_y, b_y = window.getMin()["y"] + cbz, window.getMax()["y"] - cbz
    
    # print("wmin = ({},{})".format(window.getMin()["x"], window.getMin()["y"]))
    # print("wmax = ({},{})\n".format(window.getMax()["x"], window.getMax()["y"]))

    wmin, wmax = -1, 1

    new_x = (b_x-a_x) * ((x - wmin) / (wmax - wmin)) + a_x
    new_y = (b_y-a_y) * ((y - wmin) / (wmax - wmin)) + a_y

    return {"x": new_x, "y": new_y}

  def denormalizeList(self, normalized_coords):
    coords = []
    for i in range(len(normalized_coords)):
      coords.append(self.denormalize(normalized_coords[i]["x"], normalized_coords[i]["y"]))
    return coords

  def normalizeList(self, denormalized_coords):
    coords = []
    for i in range(len(denormalized_coords)):
      coords.append(self.normalize(denormalized_coords[i]["x"], denormalized_coords[i]["y"]))
    return coords

  def translation(self, x, y, dx, dy):
    a = self.m.point(x,y)
    b = self.m.translation(dx, dy)
    
    return a.dot(b)

  def scale(self, x, y, sx, sy, cx, cy):
    a = self.m.point(x,y)
    b = self.m.translation(-cx, -cy)
    c = self.m.scaling(sx, sy)
    d = self.m.translation(cx, cy)
    
    return a.dot(b).dot(c).dot(d)

  def rotation(self, x, y, dx, dy, degrees):
    a = self.m.point(x,y)
    b = self.m.translation(-dx, -dy)
    c = self.m.rotation(degrees)
    d = self.m.translation(dx, dy)
    return a.dot(b).dot(c).dot(d)

  def center(self, coords):
    x = 0
    y = 0
    count = 0
    for i in coords:
      x += i["x"]
      y += i["y"]
      count += 1
    

    # print("cx: {} cy: {}".format(x/count, y/count))
    return {"cx": x/count, "cy": y/count}

  def move(self, tree_view, x, y):
    obj_list, index = tree_view.get_selection().get_selected()
    obj_id = obj_list[index][2]
    obj = display_file.getObject(obj_id)

    coords = obj.getNormalizedCoords()
    coords_denorm = self.denormalizeList(coords)

    for i in range(len(coords)):
      new_coords = self.translation(coords_denorm[i]["x"], coords_denorm[i]["y"], x, y)
      obj.setWorldCoords(i, new_coords[0], new_coords[1])

  def zoom(self, tree_view, sx, sy):
    obj_list, index = tree_view.get_selection().get_selected()
    obj_id = obj_list[index][2]
    obj = display_file.getObject(obj_id)

    coords = obj.getNormalizedCoords()
    coords_denorm = self.denormalizeList(coords)
    center_point = self.center(coords_denorm)

    for i in range(len(coords)):
      new_coords = self.scale(coords_denorm[i]["x"], coords_denorm[i]["y"], sx, sy, center_point["cx"], center_point["cy"])
      obj.setWorldCoords(i, new_coords[0], new_coords[1])

  def rotate(self, tree_view, degrees, rotation_type, x, y):
    obj_list, index = tree_view.get_selection().get_selected()
    obj_id = obj_list[index][2]
    obj = display_file.getObject(obj_id)

    coords = obj.getNormalizedCoords()
    coords_denorm = self.denormalizeList(coords)
    if(rotation_type == 'center'):
      point = self.center(coords_denorm)
    elif(rotation_type == 'world'):
      point = {"cx": 0, "cy": 0}
    else:
      point = {"cx": x, "cy": y}

    for i in range(len(coords)):
      new_coords = self.rotation(coords_denorm[i]["x"], coords_denorm[i]["y"], point["cx"], point["cy"], degrees)
      obj.setWorldCoords(i, new_coords[0], new_coords[1])

  def regionCode(self, x, y):
    window = Transform.window
    xw_min, xw_max = -1, 1
    yw_min, yw_max = -1, 1
    rc = np.array([0,0,0,0])
    rc[3] = 1 if (x < xw_min) else 0 
    rc[2] = 1 if (x > xw_max) else 0
    rc[1] = 1 if (y < yw_min) else 0
    rc[0] = 1 if (y > yw_max) else 0

    print(rc)