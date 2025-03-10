import numpy as np
from trimesh import Trimesh

from logic.img_logic.base import (
    GeometryCalculation,
    ImgCreator,
    Object3DGenerator,
    Object3DProcessor,
)


class ImgGenerator:
    def __init__(
        self,
        Lu,
        Lx,
        Ly,
        pixel,
        shape,
        porosity,
        misalignment,
        angle=0,
    ):
        """
        DBに登録する際は、長さをnmスケールに変換する。
        """
        self.height = 50
        self.Lu = float(Lu)  # 単位格子1辺あたりの長さ
        self.Lx = float(
            Lx
        )  # 熱電変換素子のスケールの大きさ(＊単位格子の長さではない!!)
        self.Ly = float(Ly)  # 熱電変換素子のスケールの大きさ
        self.pixel = pixel  # 画像のピクセル
        self.shape = shape  # 細孔の形状
        self.porosity = porosity  # 空隙率
        self.misalignment = misalignment  # 不整合度を調整
        self.angle = angle  # 細孔の傾き

    def _create_single_hole_object(self, Lu: float, coordinate: list) -> Trimesh:
        """細孔を作成するコード

        Args:
            Lu (float) : 単位格子一辺の長さ
            coordinate (list): 細孔の中心の座標を定義する
        """
        if self.shape == "circle":
            radious = GeometryCalculation.decide_radious(
                Lu_x=Lu, Lu_y=Lu, porosity=self.porosity, num_vertices=64
            )
            insert_object = Object3DGenerator.create_cylinder(
                radius=radious, height=self.height * 2
            )
        elif self.shape == "square":
            radious = GeometryCalculation.decide_radious(
                Lu_x=Lu, Lu_y=Lu, porosity=self.porosity, num_vertices=4
            )
            insert_object = Object3DGenerator.create_polygon_object(
                num_vertices=4, radius=radious, depth=self.height * 2, delta=self.angle
            )
        elif self.shape == "triangle":
            radious = GeometryCalculation.decide_radious(
                Lu_x=Lu, Lu_y=Lu, porosity=self.porosity, num_vertices=3
            )
            insert_object = Object3DGenerator.create_polygon_object(
                num_vertices=3, radius=radious, depth=self.height * 2, delta=self.angle
            )

        Object3DProcessor.reset_object_center_coordinate(
            insert_object, center_coordinate=coordinate
        )

        return insert_object

    def generate_film_with_single_hole(self):
        base_object = Object3DGenerator.create_cube(
            x_length=self.Lx, y_length=self.Ly, z_length=self.height
        )
        T = np.eye(4)
        # 平行移動成分を設定（右上の3×1ブロックに平行移動の値を代入）
        T[0:3, 3] = [0, 0, 0]
        base_object.apply_transform(T)
        insert_object = self._create_single_hole_object(
            Lu=self.Lu, coordinate=[self.Lx / 2, self.Ly / 2, 0]
        )
        processed_object = Object3DProcessor.subtract_mesh_from_cube(
            base_mesh=base_object, subtraction_mesh=insert_object
        )
        return processed_object

    def generate_film_with_multi_hole(self):
        base_object = Object3DGenerator.create_cube(
            x_length=self.Lx, y_length=self.Ly, z_length=self.height
        )
        T = np.eye(4)
        # 平行移動成分を設定（右上の3×1ブロックに平行移動の値を代入）
        T[0:3, 3] = [0, 0, 0]
        base_object.apply_transform(T)
        height_cf = 0
        misalignment = self.misalignment * self.Lu
        center_coordinates = []
        for grid_x in range(int(self.Lx // self.Lu)):
            for grid_y in range(int(self.Ly // self.Lu)):
                if grid_x % 2 != 0:
                    center = [
                        self.Lu * (grid_x + 0.5),
                        self.Lu * (grid_y + 0.5) + misalignment,
                        height_cf,
                    ]
                    center_coordinates.append(center)
                    if center[1] + self.Lu / 2 > self.Ly:
                        center_bottom = [
                            self.Lu * (grid_x + 0.5),
                            (center[1] - self.Ly),
                            height_cf,
                        ]
                        center_coordinates.append(center_bottom)
                else:
                    center = [
                        self.Lu * (grid_x + 0.5),
                        self.Lu * (grid_y + 0.5),
                        height_cf,
                    ]
                    center_coordinates.append(center)
        for index, center in enumerate(center_coordinates):
            hole_object = self._create_single_hole_object(Lu=self.Lu, coordinate=center)
            if index == 0:
                porous_film = Object3DProcessor.subtract_mesh_from_cube(
                    base_mesh=base_object, subtraction_mesh=hole_object
                )
            else:
                porous_film = Object3DProcessor.subtract_mesh_from_cube(
                    base_mesh=porous_film, subtraction_mesh=hole_object
                )
        return porous_film

    def create_film_picture(self, processed_object):
        plt = ImgCreator.generate_cross_section_image(
            mesh_object=processed_object,
            cube_size=self.Lx,
            hole_center_z=self.height / 2,
        )
        return plt

    def save_fig(self, plt, path):
        dpi = self.pixel / 8
        plt.savefig(path, bbox_inches="tight", pad_inches=0, dpi=dpi)

    @property
    def pixel_x_num(self):
        return self.pixel

    @property
    def pixel_y_num(self):
        return self.pixel

    @property
    def x_scale_length(self):
        return self.Lx

    @property
    def y_scale_length(self):
        return self.Ly
