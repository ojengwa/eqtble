from typing import List, Literal, Optional
from pydantic import BaseModel, field_validator


class Dimension(BaseModel):
    name: str
    type: Literal["integer", "string", "float", "date"]
    description: Optional[str] = None


class Measure(BaseModel):
    name: str
    type: Literal["integer", "float"]
    aggregation: Literal["count", "sum", "avg", "min", "max"]
    description: Optional[str] = None


class Join(BaseModel):
    dataset: str
    on: str


class View(BaseModel):
    name: str
    description: Optional[str] = None
    joins: List[Join]


class Dataset(BaseModel):
    name: str
    dimensions: List[Dimension]
    measures: List[Measure]
    views: List[View]

    @field_validator("dimensions", "measures")
    def check_unique_names(cls, v, field):
        names = [item.name for item in v]
        if len(names) != len(set(names)):
            raise ValueError(
                f"{field.name.capitalize()}: names must be unique."
            )
        return v


class Schema(BaseModel):
    dataset: Dataset
