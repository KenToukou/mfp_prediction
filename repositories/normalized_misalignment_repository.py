from models.db.mfp_models import NormalizedMisalignment
from repositories.db_repository import DBRepository
from schemas.input_schema import NormalizedMisalignmentSchema


class NormalizedMisalignmentRepository(DBRepository[NormalizedMisalignment]):
    def regist_normalized_misalignment(
        self, normalized_misalignment: NormalizedMisalignmentSchema
    ):
        normalized_misalignment = NormalizedMisalignment(
            normalized_misalignment=normalized_misalignment.normalized_misalignment
        )
        normalized_misalignment = self._merge(normalized_misalignment)
        self._commit()
        self._reflesh(record=normalized_misalignment)

    def _is_duplicate(self, normalized_misalignment: float) -> bool:
        model_filter = (
            NormalizedMisalignment.normalized_misalignment == normalized_misalignment
        )
        return self._exists(model=NormalizedMisalignment, model_filter=model_filter)

    def get_id_by_normalized_misalignment(self, normalized_misalignment):
        model_filter = (
            NormalizedMisalignment.normalized_misalignment == normalized_misalignment
        )
        response_model = self._get(model=NormalizedMisalignment, filter=model_filter)
        if response_model is not None:
            return response_model.id
        else:
            return ValueError(f"{normalized_misalignment}はテーブルに含まれてません.")
