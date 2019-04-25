from sympy import Point

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


def main():
    triangles = get_triangles_from_file("dreiecke3.txt")
    triangles = [Triangle(*triangle) for triangle in triangles]
    triangle = triangles[0]
    root: tk.Tk = tk.Tk()
    canvas_width: int = 800
    canvas_height: int = 800
    canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    triangle.show(canvas)


if __name__ == '__main__':
    main()
