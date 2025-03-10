from models.db.mfp_models import Shape
from repositories.db_repository import DBRepository
from schemas.input_schema import ShapeSchema


class ShapeRepository(DBRepository[Shape]):
    def regist_shape(self, shape: ShapeSchema):
        shape = Shape(shape=shape.shape)
        shape = self._merge(shape)
        self._commit()
        self._reflesh(record=shape)

    def _is_duplicate(self, shape: float) -> bool:
        model_filter = Shape.shape == shape
        return self._exists(model=Shape, model_filter=model_filter)

    def get_id_by_shape(self, shape):
        model_filter = Shape.shape == shape
        response_model = self._get(model=Shape, filter=model_filter)
        if response_model is not None:
            return response_model.id
        else:
            return ValueError(f"{shape}はテーブルに含まれてません.")
