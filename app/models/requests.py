from typing import Literal
from pydantic import BaseModel, Field


class AttenuationRequest(BaseModel):
    value_db: float = Field(..., ge=0.0, le=80.0)


class DopplerRequest(BaseModel):
    shift_hz: float = Field(..., ge=-200_000, le=200_000)


class MeasurementPointRequest(BaseModel):
    point: Literal["rf1", "rf2", "rf3", "rf4", "all_off"]


class PowerMeterModeRequest(BaseModel):
    mode: Literal["low_noise", "fast", "fastest"]


class SampleTimeRequest(BaseModel):
    time_us: int = Field(..., ge=10, le=1_000_000, description="Sample time in microseconds (10–1,000,000)")


class AvgCountRequest(BaseModel):
    count: int = Field(..., ge=1, le=32, description="Number of readings to average (1–32)")


class ScpiRequest(BaseModel):
    command: str = Field(..., description="Raw SCPI command string, e.g. ':SAMPLETIME?'")
