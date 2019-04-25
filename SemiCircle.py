from typing import List
from Triangle import Triangle


class SemiCircle:
    colors = ["yellow", "green", "blue", "orange", "red"]
    semi_circle_count = 0

    def __init__(self, triangles: List[Triangle]):
        self.color = self.colors[self.semi_circle_count]
        assert sum([triangle.sharpest_angle for triangle in triangles]) < 180, "Die Summe der schärfsten Winkel muss kleiner als 180 sein!"
        self.triangles: List[Triangle] = triangles

    @property
    def angle_sum(self):
        return sum([triangle.sharpest_angle for triangle in self.triangles])

    def show(self, canvas, color="black"):
        for triangle in self.triangles:
            triangle.show(canvas, color)
