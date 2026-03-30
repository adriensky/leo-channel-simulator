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
    def read_power_dbm(self) -> float:
        pass
