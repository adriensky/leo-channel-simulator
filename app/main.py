from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
from app.api.power_meter_routes import router as power_meter_router
from app.core.controller import controller

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend for the LEO Channel Simulator. "
                "Runs in mock mode locally and can later be switched to Raspberry Pi hardware mode.",
)

app.include_router(router)
app.include_router(power_meter_router)

@app.on_event("startup")
def on_startup():
    if controller.mode == "raspi":
        controller.hardware.status_led.ready()

@app.on_event("shutdown")
def on_shutdown():
    if controller.mode == "raspi":
        controller.hardware.status_led.off()
