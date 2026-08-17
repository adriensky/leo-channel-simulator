from pydantic import BaseModel


class GenericResponse(BaseModel):
    status: str
    message: str


class PowerResponse(GenericResponse):
    power_dbm: float
    measurement_point: str


class TemperatureResponse(GenericResponse):
    temperature_c: float


class DeviceInfoResponse(GenericResponse):
    model: str
    serial: str
    firmware: str


class BenchmarkResponse(GenericResponse):
    samples: int
    elapsed_s: float
    rate_hz: float
    min_dbm: float
    max_dbm: float
    mean_dbm: float


class ScpiResponse(GenericResponse):
    command: str
    response: str


class SampleTimeResponse(GenericResponse):
    time_us: int


class AvgSettingsResponse(GenericResponse):
    avg_enabled: bool
    avg_count: int


class StateResponse(BaseModel):
    signal_attenuation_db: float
    noise_attenuation_db: float
    noise_enabled: bool
    doppler_shift_hz: float
    measurement_point: str
    power_dbm: float
