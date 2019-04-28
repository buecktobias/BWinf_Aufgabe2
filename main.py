import itertools
import secrets
from math import cos, radians, sin, ceil
from typing import List, Optional
from sympy import Point

from SemiCircle import SemiCircle
from Triangle import Triangle
import tkinter as tk
from time import sleep
from knapsack_problem import Item, knapsack


def get_triangles_from_file(file_name: str):
    file = open(file_name)
    lines = file.readlines()
    polygons = []
    for line in lines[1:]:
        polygon = [int(x) for x in line.split(" ")[1:]]
        polygon = [[polygon[i - 1], polygon[i]] for i in range(1, len(polygon), 2)]
        polygons.append(polygon)
    return polygons


def calculate_triangles_angles_sum(triangles: List[Triangle]):
    return sum([triangle.sharpest_angle for triangle in triangles])


def calculate_difference_to_180(num):
    return MAXIMUM_ANGLE_SEMI_CIRCLE - num


def make_semi_circle_list(triangles):
    triangles_copy = triangles[:]
    semi_circles = []
    while len(triangles_copy) > 0:
        items = [Item(triangle, ceil(triangle.sharpest_angle)) for triangle in triangles_copy]
        max_value, picked_list = knapsack(MAXIMUM_ANGLE_SEMI_CIRCLE, items)
        best_triangles = [picked.triangle for picked in picked_list]
        semi_circles.append(SemiCircle(best_triangles))
        triangles_copy = [triangle for triangle in triangles_copy if (triangle not in best_triangles)]
    return semi_circles


def set_triangle_position_on_the_road(triangle: Triangle, point_at_which_semi_circle_is_placed, sum_of_angles_before):
    point_with_sharpest_angle =  (point_at_which_semi_circle_is_placed, STREET_Y_POSITION)
    point_at_end_of_hypotenuse = (point_with_sharpest_angle[0] - float(cos(radians(sum_of_angles_before)) * triangle.hypotenuse_length), point_with_sharpest_angle[1] + float((sin(radians(sum_of_angles_before)) * triangle.hypotenuse_length)))
    point__between_the_cathets = (point_with_sharpest_angle[0] - float((cos(radians(triangle.sharpest_angle + sum_of_angles_before)) * triangle.sharpest_angle_adjacent_length)), point_with_sharpest_angle[1] + float((sin(radians(triangle.sharpest_angle + sum_of_angles_before)) * triangle.sharpest_angle_adjacent_length)))
    triangle.a_point = Point(point_with_sharpest_angle)
    triangle.b_point = Point(point_at_end_of_hypotenuse)
    triangle.c_point = Point(point__between_the_cathets)


def is_triangle_intersecting_triangles_from_former_semi_circle(triangle, former_semi_circle: SemiCircle):
    for other_triangle in former_semi_circle.get_all_triangles_from_an_angle_of_90():
        if triangle.intersects(other_triangle):
            return True
    return False


def set_triangles_on_the_road(semi_circle_list, canvas):
    point_at_which_semi_circle_is_placed = 0
    for i, semi_circle in enumerate(semi_circle_list):
        if i == 0:
            semi_circle.triangles.sort(key=lambda triangle: triangle.hypotenuse_length, reverse=True)
        elif i == len(semi_circle_list) - 1:
            semi_circle.triangles.sort(key=lambda triangle: triangle.hypotenuse_length, reverse=False)
        else:
            semi_circle.triangles.sort(key=lambda my_triangle: my_triangle.hypotenuse_length)
            semi_circle.triangles = semi_circle_list[i].triangles[len(semi_circle_list[i].triangles) % 2::2] + semi_circle_list[i].triangles[::-2]

        if i == len(semi_circle_list) - 1:  # last semi circle
            sum_of_angles_before = 180 - semi_circle.angle_sum
        else:
            sum_of_angles_before = 0
            point_at_which_semi_circle_is_placed += semi_circle.triangles[0].hypotenuse_length

        for triangle in semi_circle.triangles:
            set_triangle_position_on_the_road(triangle, point_at_which_semi_circle_is_placed, sum_of_angles_before)
            if i > 0:
                while is_triangle_intersecting_triangles_from_former_semi_circle(triangle, semi_circle_list[i-1]):
                    point_at_which_semi_circle_is_placed += 1
                    set_triangle_position_on_the_road(triangle, point_at_which_semi_circle_is_placed, sum_of_angles_before)

            sum_of_angles_before += triangle.sharpest_angle
            triangle.show(canvas, "#" + str(secrets.token_hex(3)))
        point_at_which_semi_circle_is_placed += semi_circle.triangles[-1].sharpest_angle_adjacent_length


def main():
    triangles = get_triangles_from_file("dreiecke4.txt")
    triangles = [Triangle(*triangle) for triangle in triangles]
    root: tk.Tk = tk.Tk()
    canvas_width: int = 1000
    canvas_height: int = 800
    canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    semi_circle_list = make_semi_circle_list(triangles)
    colors = ["yellow", "red", "blue", "green", "black"]
    for counter, semi_circle in enumerate(semi_circle_list):
        semi_circle.show(canvas, colors[counter])
    set_triangles_on_the_road(semi_circle_list, canvas)
    root.mainloop()


if __name__ == '__main__':
    STREET_Y_POSITION = 400
    MAXIMUM_ANGLE_SEMI_CIRCLE = 180
    main()
