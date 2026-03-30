from fastapi import APIRouter
from app.core.controller import controller
from app.models.requests import (
    AttenuationRequest,
    NoiseEnableRequest,
    DopplerRequest,
    MeasurementPointRequest,
)
from app.models.responses import GenericResponse, PowerResponse, StateResponse

router = APIRouter(tags=["Control"])


@router.get("/health", response_model=GenericResponse)
def health() -> GenericResponse:
    return GenericResponse(
        status="ok",
        message=f"API is running in {controller.mode} mode",
    )


@router.get("/state", response_model=StateResponse)
def get_state() -> StateResponse:
    return StateResponse(**controller.get_state())


@router.post("/set_signal_attenuation", response_model=GenericResponse)
def set_signal_attenuation(req: AttenuationRequest) -> GenericResponse:
    controller.set_signal_attenuation(req.value_db)
    return GenericResponse(
        status="ok",
        message=f"Signal attenuation set to {req.value_db} dB",
    )


@router.post("/set_noise_attenuation", response_model=GenericResponse)
def set_noise_attenuation(req: AttenuationRequest) -> GenericResponse:
    controller.set_noise_attenuation(req.value_db)
    return GenericResponse(
        status="ok",
        message=f"Noise attenuation set to {req.value_db} dB",
    )


@router.post("/enable_noise", response_model=GenericResponse)
def enable_noise(req: NoiseEnableRequest) -> GenericResponse:
    controller.set_noise_enabled(req.enabled)
    state = "enabled" if req.enabled else "disabled"
    return GenericResponse(
        status="ok",
        message=f"Noise {state}",
    )


@router.post("/set_doppler", response_model=GenericResponse)
def set_doppler(req: DopplerRequest) -> GenericResponse:
    controller.set_doppler_shift(req.shift_hz)
    return GenericResponse(
        status="ok",
        message=f"Doppler shift set to {req.shift_hz} Hz",
    )


@router.post("/select_measurement_point", response_model=GenericResponse)
def select_measurement_point(req: MeasurementPointRequest) -> GenericResponse:
    controller.select_measurement_point(req.point)
    return GenericResponse(
        status="ok",
        message=f"Measurement point set to {req.point}",
    )


@router.get("/read_power", response_model=PowerResponse)
def read_power() -> PowerResponse:
    power_dbm = controller.read_power()
    state = controller.get_state()
    return PowerResponse(
        status="ok",
        message="Power read successfully",
        power_dbm=power_dbm,
        measurement_point=state["measurement_point"],
    )
