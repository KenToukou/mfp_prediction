from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from logic.db_logic.db_connect import Base


# Define the Porosity table
class Porosity(Base):
    __tablename__ = "porosity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    porosity = Column(Float, nullable=False, unique=True)
    pore_positions = relationship("PorePositionInfo", back_populates="porosity")


class Shape(Base):
    __tablename__ = "shape"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    shape = Column(String, nullable=False, unique=True)
    pore_positions = relationship("PorePositionInfo", back_populates="shape")


# Define the NormalizedMisalignment table
class NormalizedMisalignment(Base):
    __tablename__ = "normalized_misalignment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    normalized_misalignment = Column(Float, nullable=False, unique=True)
    pore_positions = relationship(
        "PorePositionInfo", back_populates="normalized_misalignment"
    )


# Define the PorePositionInfo table (junction table)
class PorePositionInfo(Base):
    __tablename__ = "pore_position_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    porosity_id = Column(Integer, ForeignKey("porosity.id"), nullable=False)
    shape_id = Column(Integer, ForeignKey("shape.id"), nullable=False)
    normalize_misalignment_id = Column(
        Integer, ForeignKey("normalized_misalignment.id"), nullable=False
    )
    porosity = relationship("Porosity", back_populates="pore_positions")
    shape = relationship("Shape", back_populates="pore_positions")
    normalized_misalignment = relationship(
        "NormalizedMisalignment", back_populates="pore_positions"
    )

    mfp = relationship("MFP", back_populates="pore_position_info")
    img = relationship("Img", back_populates="pore_position_info")


class MFP(Base):
    __tablename__ = "mfp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Thickness = Column(Float, nullable=False, unique=False)
    pore_position_id = Column(
        Integer,
        ForeignKey("pore_position_info.id"),
        nullable=False,
    )
    MSD_seed_1 = Column(Float, nullable=False)
    MSD_seed_2 = Column(Float, nullable=False)
    MSD_seed_3 = Column(Float, nullable=False)
    MSD_seed_4 = Column(Float, nullable=False)
    MSD_seed_5 = Column(Float, nullable=False)
    MSD_seed_6 = Column(Float, nullable=False)
    MSD_seed_7 = Column(Float, nullable=False)
    MSD_seed_8 = Column(Float, nullable=False)
    MSD_seed_9 = Column(Float, nullable=False)
    MSD_seed_10 = Column(Float, nullable=False)

    # Relationship back to PorePositionInfo
    pore_position_info = relationship("PorePositionInfo", back_populates="mfp")
