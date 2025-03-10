from models.db.mfp_models import Porosity
from repositories.db_repository import DBRepository
from schemas.input_schema import PorositySchema


class PorosityRepository(DBRepository[Porosity]):
    def regist_porosity(self, porosity: PorositySchema):
        porosity = Porosity(porosity=porosity.porosity)
        porosity = self._merge(porosity)
        self._commit()
        self._reflesh(record=porosity)

    def _is_duplicate(self, porosity: float) -> bool:
        model_filter = Porosity.porosity == porosity
        return self._exists(model=Porosity, model_filter=model_filter)

    def get_id_by_porosity(self, porosity):
        model_filter = Porosity.porosity == porosity
        response_model = self._get(model=Porosity, filter=model_filter)
        if response_model is not None:
            return response_model.id
        else:
            return ValueError(f"{porosity}はテーブルに含まれてません.")
