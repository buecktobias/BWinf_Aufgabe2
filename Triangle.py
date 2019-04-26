from tkinter import Canvas

from sympy import Point, Triangle as Sympy_Triangle
from mpmath import degrees


class Triangle:
    def __init__(self, a_cords, b_cords, c_cords):
        self.a_point: Point = Point(a_cords)
        self.b_point: Point = Point(b_cords)
        self.c_point: Point = Point(c_cords)
        self.tkinter_polygon = None

    @property
    def sympy_triangle(self):
        return Sympy_Triangle(self.a_point, self.b_point, self.c_point)

    @property
    def a_angle(self):
        return degrees(float(self.sympy_triangle.angles[self.a_point]))

    @property
    def b_angle(self):
        return degrees(float(self.sympy_triangle.angles[self.b_point]))

    @property
    def c_angle(self):
        return degrees(float(self.sympy_triangle.angles[self.c_point]))

    @property
    def a_length(self):
        return self.b_point.distance(self.c_point)

    @property
    def b_length(self):
        return self.a_point.distance(self.c_point)

    @property
    def c_length(self):
        return self.a_point.distance(self.b_point)

    @property
    def hypotenuse_length(self):
        return float(max(self.a_length, self.b_length, self.c_length))

    @property
    def sharpest_angle(self) -> float:
        return min(self.a_angle, self.b_angle, self.c_angle)

    @property
    def point_with_sharpest_angle(self):
        for key, value in self.sympy_triangle.angles.items():
            if degrees(float(value)) == self.sharpest_angle:
                return key

    @point_with_sharpest_angle.setter
    def point_with_sharpest_angle(self, point: Point):
        if self.point_with_sharpest_angle == self.a_point:
            self.a_point = point
        elif self.point_with_sharpest_angle == self.b_point:
            self.b_point = point
        elif self.point_with_sharpest_angle == self.c_point:
            self.c_point = point

    @property
    def sharpest_angle_adjacent_length(self):


    @property
    def opposite_sharpest_angle_length(self):
        return min(self.a_length, self.b_length, self.c_length)

    def intersects(self, other) -> bool:
        return self.sympy_triangle.intersect(other.sympy_triangle)

    def show(self, canvas: Canvas, color = "black"):
        if self.tkinter_polygon is not None:
            canvas.delete(self.tkinter_polygon)
        self.tkinter_polygon = canvas.create_polygon([round(self.a_point.x), round(self.a_point.y)], [round(self.b_point.x), round(self.b_point.y)], [round(self.c_point.x), round(self.c_point.y)], fill=color)
        canvas.pack()
        canvas.update()



