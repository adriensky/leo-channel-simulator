from app.core.state import SystemState
from app.hardware.interface import HardwareInterface
from app.drivers.awgn import NoiseGeneratorDriver
from app.drivers.rf_switch import RFSwitchDriver
from app.drivers.status_led import StatusLED
from app.drivers.power_meter import PowerMeterDriver



class RaspiHardware(HardwareInterface):
    def __init__(self, state: SystemState) -> None:
        self.state = state
        self.status_led = StatusLED(pin=5)
        self.status_led.startup()
        self.noise_generator = NoiseGeneratorDriver()
        self.rf_switch = RFSwitchDriver()
        self.power_meter = PowerMeterDriver()

        # TODO later:
        # - initialize USB attenuators
        # - initialize GPIO switch lines
        # - initialize SPI LO synthesizer
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

    def read_power_dbm(self, freq_mhz: float = 1000.0) -> float:
        power = self.power_meter.read_power_dbm(freq_mhz)
        self.state.power_dbm = power
        return power

    def get_temperature_c(self) -> float:
        return self.power_meter.get_temperature_c()

    def set_power_meter_mode(self, mode: int) -> None:
        self.power_meter.set_measurement_mode(mode)

    def get_device_info(self) -> dict:
        return {
            "model":    self.power_meter.get_model(),
            "serial":   self.power_meter.get_serial(),
            "firmware": self.power_meter.get_firmware(),
        }

    def send_scpi(self, command: str) -> str:
        return self.power_meter.send_scpi(command)

    def get_sample_time_us(self) -> int:
        return self.power_meter.get_sample_time_us()

    def set_sample_time_us(self, time_us: int) -> None:
        self.power_meter.set_sample_time_us(time_us)

    def get_avg_settings(self) -> dict:
        return {
            "avg_enabled": self.power_meter.get_avg_mode(),
            "avg_count":   self.power_meter.get_avg_count(),
        }

    def set_avg_mode(self, enabled: bool) -> None:
        self.power_meter.set_avg_mode(enabled)

    def set_avg_count(self, count: int) -> None:
        self.power_meter.set_avg_count(count)
