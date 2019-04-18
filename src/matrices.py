import numpy as np

class Matrices:
  def point(self, x, y):
    return np.array([x, y, 1])
  
  def translation(self, dx, dy):
    return np.array([[1,  0,  0],
                     [0,  1,  0],
                     [dx, dy, 1]])
