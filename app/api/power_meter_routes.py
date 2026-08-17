import time
from fastapi import APIRouter, Query
from app.core.controller import controller
from app.models.requests import (
    AvgCountRequest,
    PowerMeterModeRequest,
    SampleTimeRequest,
    ScpiRequest,
)
from app.models.responses import (
    AvgSettingsResponse,
    BenchmarkResponse,
    DeviceInfoResponse,
    GenericResponse,
    PowerResponse,
    SampleTimeResponse,
    ScpiResponse,
    TemperatureResponse,
)
from app.drivers.power_meter import MODE_LOW_NOISE, MODE_FAST, MODE_FASTEST

router = APIRouter(prefix="/power_meter", tags=["Power Meter"])


@router.get("/device_info", response_model=DeviceInfoResponse)
def device_info() -> DeviceInfoResponse:
    info = controller.get_device_info()
    return DeviceInfoResponse(
        status="ok",
        message="Device info retrieved",
        **info,
    )


@router.get("/power", response_model=PowerResponse)
def read_power(freq_mhz: float = Query(default=1000.0, ge=1.0, le=40000.0)) -> PowerResponse:
    power_dbm = controller.read_power(freq_mhz)
    state = controller.get_state()
    return PowerResponse(
        status="ok",
        message="Power read successfully",
        power_dbm=power_dbm,
        measurement_point=state["measurement_point"],
    )


@router.get("/temperature", response_model=TemperatureResponse)
def read_temperature() -> TemperatureResponse:
    temperature_c = controller.read_temperature()
    return TemperatureResponse(
        status="ok",
        message="Temperature read successfully",
        temperature_c=temperature_c,
    )


_MODE_MAP = {
    "low_noise": MODE_LOW_NOISE,
    "fast":      MODE_FAST,
    "fastest":   MODE_FASTEST,
}


@router.post("/mode", response_model=GenericResponse)
def set_power_meter_mode(req: PowerMeterModeRequest) -> GenericResponse:
    controller.set_power_meter_mode(_MODE_MAP[req.mode])
    return GenericResponse(
        status="ok",
        message=f"Power meter mode set to {req.mode}",
    )


@router.post("/scpi", response_model=ScpiResponse)
def scpi(req: ScpiRequest) -> ScpiResponse:
    response = controller.send_scpi(req.command)
    return ScpiResponse(
        status="ok",
        message="SCPI command sent",
        command=req.command,
        response=response,
    )


@router.get("/sample_time", response_model=SampleTimeResponse)
def get_sample_time() -> SampleTimeResponse:
    time_us = controller.get_sample_time_us()
    return SampleTimeResponse(
        status="ok",
        message="Sample time retrieved",
        time_us=time_us,
    )


@router.post("/sample_time", response_model=GenericResponse)
def set_sample_time(req: SampleTimeRequest) -> GenericResponse:
    controller.set_sample_time_us(req.time_us)
    return GenericResponse(
        status="ok",
        message=f"Sample time set to {req.time_us} µs",
    )


@router.get("/averaging", response_model=AvgSettingsResponse)
def get_averaging() -> AvgSettingsResponse:
    settings = controller.get_avg_settings()
    return AvgSettingsResponse(
        status="ok",
        message="Averaging settings retrieved",
        **settings,
    )


@router.post("/averaging/mode", response_model=GenericResponse)
def set_avg_mode(enabled: bool = Query(...)) -> GenericResponse:
    controller.set_avg_mode(enabled)
    return GenericResponse(
        status="ok",
        message=f"Averaging {'enabled' if enabled else 'disabled'}",
    )


@router.post("/averaging/count", response_model=GenericResponse)
def set_avg_count(req: AvgCountRequest) -> GenericResponse:
    controller.set_avg_count(req.count)
    return GenericResponse(
        status="ok",
        message=f"Average count set to {req.count}",
    )


@router.get("/benchmark", response_model=BenchmarkResponse)
def benchmark(
    samples: int = Query(default=100, ge=1, le=10000),
    freq_mhz: float = Query(default=1000.0, ge=1.0, le=40000.0),
) -> BenchmarkResponse:
    readings = []
    t0 = time.perf_counter()
    for _ in range(samples):
        readings.append(controller.read_power(freq_mhz))
    elapsed = time.perf_counter() - t0
    return BenchmarkResponse(
        status="ok",
        message=f"{samples} reads at {freq_mhz} MHz",
        samples=samples,
        elapsed_s=round(elapsed, 4),
        rate_hz=round(samples / elapsed, 2),
        min_dbm=round(min(readings), 2),
        max_dbm=round(max(readings), 2),
        mean_dbm=round(sum(readings) / len(readings), 2),
    )
