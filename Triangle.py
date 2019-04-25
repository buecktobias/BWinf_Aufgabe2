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
    def sharpest_angle(self):
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
        if self.point_with_sharpest_angle == self.a_angle:
            if self.c_length == self.hypotenuse_length:
                return self.b_length
            else:
                return self.c_length
        elif self.point_with_sharpest_angle == self.b_angle:
            if self.a_length == self.hypotenuse_length:
                return self.c_length
            else:
                return self.a_length
        else:
            if self.b_length == self.hypotenuse_length:
                return self.a_length
            else:
                return self.b_length

    @property
    def opposite_sharpest_angle_length(self):
        if self.a_point == self.point_with_sharpest_angle:
            return self.a_length
        elif self.b_point == self.point_with_sharpest_angle:
            return self.b_length
        else:
            return self.c_length

    @property
    def point_end_of_hypotenuse(self):
        if self.hypotenuse_length == self.a_length:
            if self.b_point == self.point_with_sharpest_angle:
                return self.c_point
            else:
                return self.b_point
        if self.hypotenuse_length == self.b_length:
            if self.a_point == self.point_with_sharpest_angle:
                return self.c_point
            else:
                return self.a_point
        if self.hypotenuse_length == self.c_length:
            if self.b_point == self.point_with_sharpest_angle:
                return self.b_point
            else:
                return self.a_point

    @point_end_of_hypotenuse.setter
    def point_end_of_hypotenuse(self, point: Point):
        if self.point_end_of_hypotenuse == self.c_point:
            self.c_point = point
        elif self.point_end_of_hypotenuse == self.b_point:
            self.b_point = point
        else:
            self.a_point = point

    @property
    def point_between_the_cathets(self):  # Punkt zwischen den Katheten
        if self.a_length == self.hypotenuse_length:
            return self.a_point
        elif self.b_length == self.hypotenuse_length:
            return self.b_point
        elif self.c_length == self.hypotenuse_length:
            return self.b_point

    @point_between_the_cathets.setter
    def point_between_the_cathets(self, point: Point):
        if self.point_between_the_cathets == self.a_point:
            self.a_point = point
        elif self.point_between_the_cathets == self.b_point:
            self.b_point = point
        else:
            self.c_point = point

    def intersects(self, other) -> bool:
        return self.sympy_triangle.intersect(other.sympy_triangle)

    def show(self, canvas: Canvas):
        if self.tkinter_polygon is not None:
            canvas.delete(self.tkinter_polygon)
        self.tkinter_polygon = canvas.create_polygon([self.a_point.x, self.a_point.y], [self.b_point.x, self.b_point.y], [self.c_point.x, self.c_point.y])
        canvas.pack()
        canvas.update()



