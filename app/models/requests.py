from typing import Literal
from pydantic import BaseModel, Field


class AttenuationRequest(BaseModel):
    value_db: float = Field(..., ge=0.0, le=80.0)


class DopplerRequest(BaseModel):
    shift_hz: float = Field(..., ge=-200_000, le=200_000)


class MeasurementPointRequest(BaseModel):
    point: Literal["rf1", "rf2", "rf3", "rf4", "all_off"]
