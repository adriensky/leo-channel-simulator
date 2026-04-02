from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    sim_mode: str = os.getenv("SIM_MODE", "mock").lower()
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    app_name: str = os.getenv("APP_NAME", "LEO Channel Simulator API")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")

    # Noise generator TTL
    noise_generator_ttl_pin: int = int(os.getenv("NOISE_GEN_TTL_PIN", "17"))
    noise_generator_active_high: bool = os.getenv(
        "NOISE_GEN_ACTIVE_HIGH", "true"
    ).lower() == "true"

    rf_switch_v1_pin: int = int(os.getenv("RF_SWITCH_V1_PIN", "22"))
    rf_switch_v2_pin: int = int(os.getenv("RF_SWITCH_V2_PIN", "23"))
    rf_switch_v3_pin: int = int(os.getenv("RF_SWITCH_V3_PIN", "24"))


settings = Settings()
