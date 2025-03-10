from models.db.mfp_models import PorePositionInfo
from repositories.db_repository import DBRepository


class PorePositionRepository(DBRepository[PorePositionInfo]):
    def regist_pore_position(self, porosity_id, shape_id, normalized_misalignment_id):
        pore_position = PorePositionInfo(
            porosity_id=porosity_id,
            shape_id=shape_id,
            normalize_misalignment_id=normalized_misalignment_id,
        )
        pore_position = self._merge(pore_position)
        self._commit()
        self._reflesh(record=pore_position)

    def get_id_by_porosity_info(
        self, porosity_id, shape_id, normalized_misalignment_id
    ):
        model_filter = PorePositionInfo.porosity_id == porosity_id
        model_filter &= PorePositionInfo.shape_id == shape_id
        model_filter &= (
            PorePositionInfo.normalize_misalignment_id == normalized_misalignment_id
        )
        response_model = self._get(model=PorePositionInfo, filter=model_filter)
        if response_model is not None:
            return response_model.id
        else:
            return ValueError("入力されたデータはテーブルに含まれてません.")

    def get_mfp_data(
        self,
        porosity_id=None,
        shape_id=None,
        normalized_misalignment_id=None,
    ):
        pass
