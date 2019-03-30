from gi.repository import Gtk
from shapes.point import Point
from shapes.line import Line

class Handler:
  def __init__(self, builder):
    self.builder = builder

  def onDestroy(self, *args):
    Gtk.main_quit()

  def onButtonPressed(self, button):
    print("Hello World!")
  
  def openAddObjectWindow(self, button):
    add_object_window = self.builder.get_object("AddObjectWindow")
    add_object_window.show_all()

  def addPoint(self, button):
    name_entry = self.builder.get_object("PointNameEntry")
    x_entry = self.builder.get_object("PointXEntry")
    y_entry = self.builder.get_object("PointYEntry")
    p1 = Point(name_entry.get_text())
    p1.addCoords(x_entry.get_text(), y_entry.get_text())

  def addLine(self, button):
    name_entry = self.builder.get_object("EntryNameNewLine")
    x1_entry = self.builder.get_object("EntryX1Line")
    y1_entry = self.builder.get_object("EntryY1Line")
    x2_entry = self.builder.get_object("EntryX2Line")
    y2_entry = self.builder.get_object("EntryY2Line")
    l1 = Line(name_entry.get_text())
    l1.addCoords(x1_entry.get_text(), y1_entry.get_text())
    l1.addCoords(x2_entry.get_text(), y2_entry.get_text())