from abc import ABC, abstractmethod


class HardwareInterface(ABC):
    @abstractmethod
    def set_signal_attenuation(self, value_db: float) -> None:
        pass

    @abstractmethod
    def set_noise_attenuation(self, value_db: float) -> None:
        pass

    @abstractmethod
    def set_noise_enabled(self, enabled: bool) -> None:
        pass

    @abstractmethod
    def set_doppler_shift(self, shift_hz: float) -> None:
        pass

    @abstractmethod
    def set_measurement_point(self, point: str) -> None:
        pass

    @abstractmethod
    def read_power_dbm(self, freq_mhz: float = 1000.0) -> float:
        pass

    @abstractmethod
    def get_temperature_c(self) -> float:
        pass

    @abstractmethod
    def set_power_meter_mode(self, mode: int) -> None:
        pass

    @abstractmethod
    def get_device_info(self) -> dict:
        pass

    @abstractmethod
    def send_scpi(self, command: str) -> str:
        pass

    @abstractmethod
    def get_sample_time_us(self) -> int:
        pass

    @abstractmethod
    def set_sample_time_us(self, time_us: int) -> None:
        pass

    @abstractmethod
    def get_avg_settings(self) -> dict:
        pass

    @abstractmethod
    def set_avg_mode(self, enabled: bool) -> None:
        pass

    @abstractmethod
    def set_avg_count(self, count: int) -> None:
        pass
