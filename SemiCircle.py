from typing import List
from Triangle import Triangle


class SemiCircle:
    max_value = 180

    def __init__(self):
        self.triangles: List[Triangle] = []

    def add_triangle(self, triangle: Triangle):
        assert self.can_triangle_be_added(triangle), "Triangle can not be added !!!"
        self.triangles.append(triangle)

    def can_triangle_be_added(self, triangle:Triangle):
        return self.angle_sum + triangle.sharpest_angle < self.max_value

    @property
    def angle_sum(self):
        return sum([triangle.sharpest_angle for triangle in self.triangles])

    def show(self, canvas, color="black"):
        for triangle in self.triangles:
            triangle.show(canvas, color)

    def get_all_triangles_from_an_angle_of_90(self) -> List[Triangle]:  # gibt alle Dreiecke zurück
        current_degree = 0
        triangles_from_an_angle_of_90: List[Triangle] = []
        for triangle in self.triangles:
            current_degree += triangle.sharpest_angle
            if current_degree > 90:
                triangles_from_an_angle_of_90.append(triangle)
        return triangles_from_an_angle_of_90
