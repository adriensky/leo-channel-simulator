from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    sim_mode: str = os.getenv("SIM_MODE", "mock").lower()
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    app_name: str = os.getenv("APP_NAME", "LEO Channel Simulator API")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")


settings = Settings()
