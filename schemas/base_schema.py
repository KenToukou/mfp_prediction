import pydantic
from pydantic import validator


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True
        extra = "ignore"

    @validator("*", pre=True, always=True)
    def empty_name_to_none(cls, v):
        return None if v == "" else v
