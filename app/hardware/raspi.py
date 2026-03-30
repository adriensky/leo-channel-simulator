from app.core.state import SystemState
from app.hardware.interface import HardwareInterface


class RaspiHardware(HardwareInterface):
    def __init__(self, state: SystemState) -> None:
        self.state = state
        # TODO later:
        # - initialize USB attenuators
        # - initialize GPIO switch lines
        # - initialize GPIO noise enable
        # - initialize SPI LO synthesizer
        # - initialize USB power meter
        # - initialize USB-RS485 adapter

    def set_signal_attenuation(self, value_db: float) -> None:
        self.state.signal_attenuation_db = value_db
        # TODO: send command to signal attenuator via USB

    def set_noise_attenuation(self, value_db: float) -> None:
        self.state.noise_attenuation_db = value_db
        # TODO: send command to noise attenuator via USB

    def set_noise_enabled(self, enabled: bool) -> None:
        self.state.noise_enabled = enabled
        # TODO: toggle GPIO for AWGN source

    def set_doppler_shift(self, shift_hz: float) -> None:
        self.state.doppler_shift_hz = shift_hz
        # TODO: compute LO frequency and send via SPI

    def set_measurement_point(self, point: str) -> None:
        self.state.measurement_point = point
        # TODO: drive GPIO truth table for SP4T switch

    def read_power_dbm(self) -> float:
        # TODO: read from USB power meter
        return self.state.power_dbm
