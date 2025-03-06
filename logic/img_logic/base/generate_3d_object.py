import numpy as np
import trimesh
from trimesh import Trimesh


class Object3DGenerator:
    @classmethod
    def create_cube(cls, x_length, y_length, z_length) -> Trimesh:
        box_bounds = np.array([[0, 0, 0], [x_length, y_length, z_length]])
        return trimesh.creation.box(bounds=box_bounds)

    @classmethod
    def create_cylinder(cls, radius, height, segments=64) -> Trimesh:
        return trimesh.creation.cylinder(
            radius=radius, height=height, sections=segments
        )

    @classmethod
    def create_polygon_object(cls, num_vertices, radius, depth, delta=0) -> Trimesh:
        angle_step = 2 * np.pi / num_vertices
        points = []
        r = radius
        for i in range(num_vertices):
            angle = (i * angle_step) + (np.pi / num_vertices) + delta
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append((x, y))
        polygon = trimesh.path.polygons.Polygon(points)
        return trimesh.creation.extrude_polygon(polygon, height=depth)


class Object3DProcessor:
    @classmethod
    def subtract_mesh_from_cube(
        base_mesh: Trimesh, subtraction_mesh: Trimesh
    ) -> Trimesh:
        processed_mesh = base_mesh.difference(subtraction_mesh)
        return processed_mesh

    @classmethod
    def reset_object_center_coordinate(
        cls, mesh_object: Trimesh, center_coordinate: list
    ):
        mesh_object.apply_translation(center_coordinate)
        return mesh_object
