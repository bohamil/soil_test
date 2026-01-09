from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class APIBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GroupCreate(BaseModel):
    user_id: int
    name: str


class GroupUpdate(BaseModel):
    name: str


class Group(APIBase):
    id: int
    user_id: int
    name: str
    created_at: datetime


class FieldCreate(BaseModel):
    user_id: int
    group_id: int | None = None
    field_name: str
    geometry_wkt: str | None = None
    source_file_name: str | None = None
    attributes_json: dict[str, Any] | None = None


class FieldUpdate(BaseModel):
    group_id: int | None = None
    field_name: str | None = None
    geometry_wkt: str | None = None
    source_file_name: str | None = None
    attributes_json: dict[str, Any] | None = None


class Field(APIBase):
    id: int
    user_id: int
    group_id: int | None
    field_name: str
    geometry_wkt: str | None
    source_file_name: str | None
    attributes_json: dict[str, Any] | None
    created_at: datetime


class SamplingPlanCreate(BaseModel):
    name: str
    grid_size_acres: float = Field(ge=0.1)
    grid_offset_x: float = 0.0
    grid_offset_y: float = 0.0
    numbering_method: str = "snake"


class SamplingPlan(APIBase):
    id: int
    field_id: int
    name: str
    grid_size_acres: float
    grid_offset_x: float
    grid_offset_y: float
    numbering_method: str
    created_at: datetime


class SamplingPointCreate(BaseModel):
    point_index: int = Field(ge=1)
    geometry_wkt: str
    properties_json: dict[str, Any] | None = None


class SamplingPoint(APIBase):
    id: int
    sampling_plan_id: int
    point_index: int
    geometry_wkt: str
    properties_json: dict[str, Any] | None


class LabUploadCreate(BaseModel):
    original_filename: str
    mapping_json: dict[str, Any] | None = None


class LabUpload(APIBase):
    id: int
    sampling_plan_id: int
    original_filename: str
    mapping_json: dict[str, Any] | None
    created_at: datetime
