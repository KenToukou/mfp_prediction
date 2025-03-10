from .base_schema import BaseModel


class PorositySchema(BaseModel):
    porosity: float


class ShapeSchema(BaseModel):
    shape: str


class NormalizedMisalignmentSchema(BaseModel):
    normalized_misalignment: float


class ExperimentInputSchema(BaseModel):
    pore_position_id: int
    height: float


class MFPInputSchema(BaseModel):
    experiment_id: int
    mfp: float
    seed_number: int
