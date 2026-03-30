from pydantic import BaseModel


class GenericResponse(BaseModel):
    status: str
    message: str


class PowerResponse(GenericResponse):
    power_dbm: float
    measurement_point: str


class StateResponse(BaseModel):
    signal_attenuation_db: float
    noise_attenuation_db: float
    noise_enabled: bool
    doppler_shift_hz: float
    measurement_point: str
    power_dbm: float
