import pandas as pd
from sqlalchemy import text

from logic.db_logic.db_connect import get_db_session

from .sql_queries import (
    GET_ALL_MFP_DATA,
    GET_ALL_PORE_POSITION_INF,
    GET_IMG_INF,
    GET_MFP_DATA,
    GET_PORE_INF_ID,
    UPDATE_MFP_DATA,
)


class DBService:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def get_all_msd_data(self):
        query = GET_ALL_MFP_DATA
        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query,
            )
            response = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(response, columns=columns)
        return df

    def get_msd_data(self, shape, porosity, normalized_misalignment):

        query_1 = GET_MFP_DATA

        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query_1,
                {
                    "shape": shape,
                    "porosity": porosity,
                    "normalized_misalignment": normalized_misalignment,
                },
            )
            response = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(response, columns=columns)

        return df

    def update_mfp_data(self, shape, porosity, normalized_misalignment, df):

        query_update = UPDATE_MFP_DATA

        # DataFrame から実際に更新するパラメータのリストを生成
        update_params_list = []
        for idx, row in df.iterrows():
            # カラム名は実際の DataFrame の列名に合わせて修正してください
            update_params_list.append(
                {
                    "shape": shape,
                    "porosity": porosity,
                    "normalized_misalignment": normalized_misalignment,
                    "thickness": row["Thickness"],
                    "MSD_seed_1": row["MSD_seed_1"],
                    "MSD_seed_2": row["MSD_seed_2"],
                    "MSD_seed_3": row["MSD_seed_3"],
                    "MSD_seed_4": row["MSD_seed_4"],
                    "MSD_seed_5": row["MSD_seed_5"],
                    "MSD_seed_6": row["MSD_seed_6"],
                    "MSD_seed_7": row["MSD_seed_7"],
                    "MSD_seed_8": row["MSD_seed_8"],
                    "MSD_seed_9": row["MSD_seed_9"],
                    "MSD_seed_10": row["MSD_seed_10"],
                }
            )

        if not update_params_list:
            # DataFrame が空の場合は何もせず True で返す、などの処理でもOK
            return True

        with get_db_session(self.db_url) as cursor:
            # executemanyでまとめて UPDATE
            cursor.executemany(query_update, update_params_list)
            # コミットが必要な場合
            # cursor.connection.commit()
        return True

    def delete_mfp_by_id(self, pore_info_id: float):
        delete_query = text(
            """
            DELETE FROM mfp
            WHERE pore_position_id = :pore_info_id
        """
        )
        with get_db_session(self.db_url) as session:
            result = session.execute(delete_query, {"pore_info_id": pore_info_id})
            session.commit()  # DELETE 文の実行後はコミットが必要
            deleted_rows = result.rowcount

        return deleted_rows

    def get_pore_position_id(self, shape, porosity, normalized_misalignment):
        query = GET_PORE_INF_ID
        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query,
                {
                    "shape": shape,
                    "porosity": porosity,
                    "normalized_misalignment": normalized_misalignment,
                },
            )
            response = result.fetchall()

        return float(response[0][0])

    def post_data_to_img_db(self, df: pd.DataFrame):
        with get_db_session(self.db_url) as session:
            engine = session.bind
            df.to_sql("img", con=engine, if_exists="append", index=False)
        return True

    def is_img_in_db(
        self,
        shape,
        porosity,
        normalized_misalignment,
        pixel_x_num,
        pixel_y_num,
        x_scale_length,
        y_scale_length,
    ):
        query = GET_IMG_INF
        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query,
                {
                    "shape": shape,
                    "porosity": porosity,
                    "normalized_misalignment": normalized_misalignment,
                    "pixel_x_num": pixel_x_num,
                    "pixel_y_num": pixel_y_num,
                    "x_scale_length": x_scale_length,
                    "y_scale_length": y_scale_length,
                },
            )
            response = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(response, columns=columns)
        return df.shape[0] != 0

    def get_all_pore_position_inf(self):
        query = GET_ALL_PORE_POSITION_INF
        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query,
            )
            response = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(response, columns=columns)
        return df

    def get_img_data_from_db(
        self,
        shape,
        porosity,
        normalized_misalignment,
        pixel_x_num,
        pixel_y_num,
        x_scale_length,
        y_scale_length,
    ):
        query = GET_IMG_INF
        with get_db_session(self.db_url) as cursor:
            # パラメータを辞書形式で渡す
            result = cursor.execute(
                query,
                {
                    "shape": shape,
                    "porosity": porosity,
                    "normalized_misalignment": normalized_misalignment,
                    "pixel_x_num": pixel_x_num,
                    "pixel_y_num": pixel_y_num,
                    "x_scale_length": x_scale_length,
                    "y_scale_length": y_scale_length,
                },
            )
            response = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(response, columns=columns)
        return df.shape[0] != 0
