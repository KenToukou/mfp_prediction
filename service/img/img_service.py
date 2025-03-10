import pandas as pd

from logic.img_logic.generate_img import ImgGenerator
from service.db.db_service import DBService


class ImgService:
    @classmethod
    def regist_img(cls, db_api: DBService, img_class: ImgGenerator):
        path = None

        query_dict: dict = {
            "shape": img_class.shape,
            "porosity": img_class.porosity,
            "normalized_misalignment": img_class.misalignment,
            "pixel_x_num": img_class.pixel_x_num,
            "pixel_y_num": img_class.pixel_y_num,
            "x_scale_length": img_class.x_scale_length,
            "y_scale_length": img_class.y_scale_length,
        }
        if db_api.is_img_in_db(**query_dict) is False:
            print("新規作成")
            path = (
                f"./fig/data/{img_class.shape}_{img_class.porosity}_{img_class.misalignment}_"
                f"pixx{img_class.pixel_x_num}_x{img_class.x_scale_length}_y{img_class.y_scale_length}.png"
            )
            print("画像を保存")
            processed_object = img_class.generate_film_with_multi_hole()
            plt = img_class.create_film_picture(processed_object)
            img_class.save_fig(plt, path=path)
            print("完了")
            print("DBへデータを保存")
            pore_id = db_api.get_pore_position_id(
                shape=img_class.shape,
                porosity=img_class.porosity,
                normalized_misalignment=img_class.misalignment,
            )
            input_df = pd.DataFrame(
                [
                    {
                        "pore_position_id": pore_id,
                        "pixel_x_num": img_class.pixel_x_num,
                        "pixel_y_num": img_class.pixel_y_num,
                        "x_scale_length": img_class.x_scale_length,
                        "y_scale_length": img_class.y_scale_length,
                        "img_path": path,
                    }
                ]
            )
            db_api.post_data_to_img_db(df=input_df)
            print("完了")

        else:
            print("already exist.")
