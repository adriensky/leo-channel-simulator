from fastapi import FastAPI
from app.config import settings
from app.api.routes import router
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
