from app.config import settings
from app.core.state import SystemState
from app.hardware.interface import HardwareInterface
from app.hardware.mock import MockHardware
from app.hardware.raspi import RaspiHardware


class Controller:
    def __init__(self) -> None:
        self.mode = settings.sim_mode
        self.state = SystemState()

        if self.mode == "raspi":
            self.hardware: HardwareInterface = RaspiHardware(self.state)
        else:
            self.hardware = MockHardware(self.state)

    def get_state(self) -> dict:
        return self.state.to_dict()

    def set_signal_attenuation(self, value_db: float) -> None:
        self.hardware.set_signal_attenuation(value_db)

    def set_noise_attenuation(self, value_db: float) -> None:
        self.hardware.set_noise_attenuation(value_db)

    def set_noise_enabled(self, enabled: bool) -> None:
        self.hardware.set_noise_enabled(enabled)

    def set_doppler_shift(self, shift_hz: float) -> None:
        self.hardware.set_doppler_shift(shift_hz)

    def select_measurement_point(self, point: str) -> None:
        self.hardware.set_measurement_point(point)

    def read_power(self) -> float:
        return self.hardware.read_power_dbm()


controller = Controller()
