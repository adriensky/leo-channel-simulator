from app.config import settings
from app.core.state import SystemState
from app.hardware.interface import HardwareInterface
from app.hardware.mock import MockHardware
from app.hardware.raspi import RaspiHardware


class Controller:
    ATTENUATION_MIN_DB = 0.0
    ATTENUATION_MAX_DB = 80.0
    ATTENUATION_STEP_DB = 0.25

    def __init__(self) -> None:
        self.mode = settings.sim_mode
        self.state = SystemState()

        if self.mode == "raspi":
            self.hardware: HardwareInterface = RaspiHardware(self.state)
        else:
            self.hardware = MockHardware(self.state)

    def get_state(self) -> dict:
        return self.state.to_dict()

    def _normalize_attenuation(self, value_db: float) -> float:
        # Clamp to valid range
        value_db = max(self.ATTENUATION_MIN_DB, min(self.ATTENUATION_MAX_DB, value_db))
        # Round to nearest 0.25 dB
        value_db = round(value_db / self.ATTENUATION_STEP_DB) * self.ATTENUATION_STEP_DB
        # Avoid floating-point artifacts
        return round(value_db, 2)

    def set_signal_attenuation(self, value_db: float) -> float:
        normalized = self._normalize_attenuation(value_db)
        self.hardware.set_signal_attenuation(normalized)
        return normalized

    def set_noise_attenuation(self, value_db: float) -> float:
        normalized = self._normalize_attenuation(value_db)
        self.hardware.set_noise_attenuation(normalized)
        return normalized

    def set_noise_enabled(self, enabled: bool) -> None:
        self.hardware.set_noise_enabled(enabled)

    def enable_noise(self) -> None:
        self.hardware.set_noise_enabled(True)

    def disable_noise(self) -> None:
        self.hardware.set_noise_enabled(False)

    def set_doppler_shift(self, shift_hz: float) -> None:
        self.hardware.set_doppler_shift(shift_hz)

    def select_measurement_point(self, point: str) -> None:
        self.hardware.set_measurement_point(point)

    def read_power(self) -> float:
        return self.hardware.read_power_dbm()


controller = Controller()
