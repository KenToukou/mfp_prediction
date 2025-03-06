from logic.db_logic.db_connect import Base, get_db_engine
from models.db import (  # noqa
    MFP,
    Img,
    NormalizedMisalignment,
    PorePositionInfo,
    Porosity,
    Shape,
)


def create_db(db_url: str) -> None:
    engine = get_db_engine(db_url)
    Base.metadata.create_all(bind=engine)
    print("Successfully created the db")
