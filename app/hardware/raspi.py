from app.core.state import SystemState
from app.hardware.interface import HardwareInterface
from app.drivers.awgn import NoiseGeneratorDriver
from app.drivers.rf_switch import RFSwitchDriver



class RaspiHardware(HardwareInterface):
    def __init__(self, state: SystemState) -> None:
        self.state = state
        self.noise_generator = NoiseGeneratorDriver()
        self.rf_switch = RFSwitchDriver()


        # TODO later:
        # - initialize USB attenuators
        # - initialize GPIO switch lines
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
        if enabled:
            self.noise_generator.enable()            
        else:
            self.noise_generator.disable()
        self.state.noise_enabled = enabled

    def set_doppler_shift(self, shift_hz: float) -> None:
        self.state.doppler_shift_hz = shift_hz
        # TODO: compute LO frequency and send via SPI

    def set_measurement_point(self, point: str) -> None:
        point_upper = point.upper()

        if point_upper == "RF1":
            self.rf_switch.select_rf1()
        elif point_upper == "RF2":
            self.rf_switch.select_rf2()
        elif point_upper == "RF3":
            self.rf_switch.select_rf3()
        elif point_upper == "RF4":
            self.rf_switch.select_rf4()
        elif point_upper == "ALL_OFF":
            self.rf_switch.all_off()
        else:
            raise ValueError(f"Unsupported measurement point: {point}")

        self.state.measurement_point = point_upper

    def read_power_dbm(self) -> float:
        # TODO: read from USB power meter
        return self.state.power_dbm
