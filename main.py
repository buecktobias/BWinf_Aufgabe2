import itertools
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
    print("END")
    root.mainloop()


if __name__ == '__main__':
    main()
