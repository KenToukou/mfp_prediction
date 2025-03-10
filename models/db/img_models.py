from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from logic.db_logic.db_connect import Base


class Img(Base):
    __tablename__ = "img"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pore_position_id = Column(
        Integer,
        ForeignKey("pore_position_info.id"),
        nullable=False,
    )

    pixel_x_num = Column(
        Float, nullable=False
    )  # ピクセル(画像の解像度の情報 xとyは等しくなる)
    pixel_y_num = Column(Float, nullable=False)  # ピクセル(画像の解像度の情報)
    x_scale_length = Column(Float, nullable=False)  # 熱電変換素子のスケール長さ
    y_scale_length = Column(Float, nullable=False)  # 熱電変換素子のスケール長さ
    img_path = Column(String, nullable=False)

    # Relationship back to PorePositionInfo
    pore_position_info = relationship("PorePositionInfo", back_populates="img")
