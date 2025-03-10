import matplotlib.pyplot as plt
from trimesh import Trimesh


class ImgCreator:
    @classmethod
    def generate_cross_section_image(
        cls,
        mesh_object: Trimesh,
        cube_size,
        hole_center_z,
        outer_edge_color="black",
        outer_face_color="black",
        inner_edge_color="black",
        inner_facecolor="white",
        title="",
    ):
        slice_plane_origin = [cube_size / 2, cube_size / 2, hole_center_z]
        slice_plane_normal = [0, 0, 1]

        print("Slice plane origin:", slice_plane_origin)
        print("Slice plane normal:", slice_plane_normal)

        slice_section = mesh_object.section(
            plane_origin=slice_plane_origin, plane_normal=slice_plane_normal
        )
        plt.figure(figsize=(8, 8))

        if slice_section is not None:
            # 断面を2D平面に投影
            slice_2D, to_3D = slice_section.to_planar()

            # 断面の輪郭を取得してプロット
            # polygons_full は Shapely の Polygon オブジェクトのリスト
            for polygon in slice_2D.polygons_full:
                x, y = polygon.exterior.coords.xy
                plt.fill(
                    x,
                    y,
                    linewidth=1,
                    edgecolor=outer_edge_color,
                    facecolor=outer_face_color,
                )

                # 内部の穴（もしあれば）を塗りつぶす
                for interior in polygon.interiors:
                    ix, iy = interior.coords.xy
                    plt.fill(
                        ix,
                        iy,
                        linewidth=1,
                        edgecolor=inner_edge_color,
                        facecolor=inner_facecolor,
                    )

            plt.gca().set_aspect("equal")

            plt.xlabel("X")
            plt.ylabel("Y")

            plt.axis("off")
            plt.gca().set_aspect("equal")
            return plt
        else:
            print("Failed to obtain cross-section.")
