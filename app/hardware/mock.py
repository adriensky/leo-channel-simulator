from app.core.state import SystemState
from app.hardware.interface import HardwareInterface


class MockHardware(HardwareInterface):
    def __init__(self, state: SystemState) -> None:
        self.state = state

    def set_signal_attenuation(self, value_db: float) -> None:
        self.state.signal_attenuation_db = value_db
        self._update_mock_power()

    def set_noise_attenuation(self, value_db: float) -> None:
        self.state.noise_attenuation_db = value_db
        self._update_mock_power()

    def set_noise_enabled(self, enabled: bool) -> None:
        self.state.noise_enabled = enabled
        self._update_mock_power()

    def set_doppler_shift(self, shift_hz: float) -> None:
        self.state.doppler_shift_hz = shift_hz

    def set_measurement_point(self, point: str) -> None:
        self.state.measurement_point = point
        self._update_mock_power()

    def read_power_dbm(self, freq_mhz: float = 1000.0) -> float:
        self._update_mock_power()
        return self.state.power_dbm

    def get_temperature_c(self) -> float:
        return 25.0

    def set_power_meter_mode(self, mode: int) -> None:
        pass

    def get_device_info(self) -> dict:
        return {"model": "MOCK-PWR", "serial": "000000", "firmware": "M1"}

    def send_scpi(self, command: str) -> str:
        return "0"

    def get_sample_time_us(self) -> int:
        return 1000

    def set_sample_time_us(self, time_us: int) -> None:
        pass

    def get_avg_settings(self) -> dict:
        return {"avg_enabled": False, "avg_count": 1}

    def set_avg_mode(self, enabled: bool) -> None:
        pass

    def set_avg_count(self, count: int) -> None:
        pass

    def _update_mock_power(self) -> None:
        # Simple mock model:
        # Higher signal attenuation lowers measured power.
        # Enabled noise slightly worsens the apparent reading.
        base_signal_dbm = -10.0 - self.state.signal_attenuation_db

        noise_penalty = 0.0
        if self.state.noise_enabled:
            noise_penalty = min(self.state.noise_attenuation_db / 10.0, 10.0)

        measurement_offsets = {
            "rf1": 0.0,
            "rf2": -1.0,
            "rf3": -2.0,
            "rf4": -3.0,
            "off": -120.0,
        }

        self.state.power_dbm = (
            base_signal_dbm
            - noise_penalty
            + measurement_offsets.get(self.state.measurement_point, -120.0)
        )
