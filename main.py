import itertools
from math import cos, radians, sin
from typing import List, Optional

from sympy import Point

from SemiCircle import SemiCircle
from Triangle import Triangle
import tkinter as tk
from time import sleep


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
    return 180 - num


def make_semi_circle_list_combination(triangles):
    triangles_copy: List[Triangle] = triangles[:]
    semi_circle_list = []
    while len(triangles_copy) > 0:
        print(" while")
        best_triangle_difference = 180
        best_triangles: Optional[List[Triangle]] = None

        for n in range(1, len(triangles)):
            combinated_triangles = itertools.combinations(triangles, n)
            for triangle_combination in combinated_triangles:
                if calculate_difference_to_180(calculate_triangles_angles_sum(list(triangle_combination))) < 0:  # Wenn die Dreiecke mehr als 180 Grad haben, wird die Kombination übersprungen
                    continue
                if calculate_difference_to_180(calculate_triangles_angles_sum(list(triangle_combination))) < best_triangle_difference:
                    best_triangles: List[Triangle] = list(triangle_combination)
                    best_triangle_difference = calculate_difference_to_180(calculate_triangles_angles_sum(list(triangle_combination)))

        triangles_copy = [triangle for triangle in triangles_copy if(triangle not in best_triangles)]  # removes all triangles of best_triangles
        semi_circle_list.append(SemiCircle(best_triangles))
    return semi_circle_list


def make_semi_circle_list(triangles):
    triangles_copy: List[Triangle] = triangles[:]
    semi_circle_list = []
    while len(triangles_copy) > 0:
        best_triangles = triangles_copy[:]
        while calculate_triangles_angles_sum(best_triangles) > 180:
            best_triangles.pop()
        triangles_copy = [triangle for triangle in triangles_copy if (triangle not in best_triangles)]
        semi_circle_list.append(SemiCircle(best_triangles))
    return semi_circle_list


# TODO triangle naming counter clockwise
def set_triangle_position_on_the_road(triangle: Triangle, point_at_which_semi_circle_is_placed, sum_of_angles_before):
    point_with_sharpest_angle =  (point_at_which_semi_circle_is_placed, STREET_Y_POSITION)
    point_at_end_of_hypotenuse = (point_with_sharpest_angle[0] - float(cos(radians(sum_of_angles_before)) * triangle.hypotenuse_length), point_with_sharpest_angle[1] + float((sin(radians(sum_of_angles_before)) * triangle.hypotenuse_length)))
    point__between_the_cathets = (point_with_sharpest_angle[0] - float((cos(radians(triangle.sharpest_angle + sum_of_angles_before)) * triangle.sharpest_angle_adjacent_length)), point_with_sharpest_angle[1] + float((sin(radians(triangle.sharpest_angle + sum_of_angles_before)) * triangle.sharpest_angle_adjacent_length)))
    triangle.a_point = Point(point_with_sharpest_angle)
    triangle.b_point = Point(point_at_end_of_hypotenuse)
    triangle.c_point = Point(point__between_the_cathets)


def set_triangles_on_the_road(semi_circle_list, canvas):
    point_at_which_semi_circle_is_placed = 0
    for i, semi_circle in enumerate(semi_circle_list):
        if i == 0:
            semi_circle.triangles.sort(key=lambda triangle: triangle.hypotenuse_length)
        elif i == len(semi_circle_list) - 1:
            semi_circle.triangles.sort(key=lambda triangle: triangle.hypotenuse_length, reverse=True)
        else:
            semi_circle.triangles.sort(key=lambda my_triangle: my_triangle.hypotenuse_length)
            semi_circle.triangles = semi_circle_list[i].triangles[len(semi_circle_list[i].triangles) % 2::2] + semi_circle_list[i].triangles[::-2]

    if i == len(semi_circle_list) - 1:  # last semi circle
        sum_of_angles_before = 180 - semi_circle.angle_sum
    else:
        sum_of_angles_before = 0
        point_at_which_semi_circle_is_placed += semi_circle_list[i].triangles[0].hypotenuse_length

    for triangle in semi_circle.triangles:
        set_triangle_position_on_the_road(triangle, point_at_which_semi_circle_is_placed, sum_of_angles_before)
        sum_of_angles_before += triangle.sharpest_angle
        triangle.show(canvas)


def main():
    triangles = get_triangles_from_file("dreiecke3.txt")
    triangles = [Triangle(*triangle) for triangle in triangles]
    triangle = triangles[0]
    root: tk.Tk = tk.Tk()
    canvas_width: int = 800
    canvas_height: int = 800
    canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    triangle.show(canvas)
    semi_circle_list = make_semi_circle_list(triangles)
    colors = ["yellow", "red", "blue"]
    for counter, semi_circle in enumerate(semi_circle_list):
        print(calculate_triangles_angles_sum(semi_circle.triangles))
        semi_circle.show(canvas, colors[counter])
    set_triangles_on_the_road(semi_circle_list, canvas)
    root.mainloop()


if __name__ == '__main__':
    STREET_Y_POSITION = 200
    main()
