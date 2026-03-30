from dataclasses import dataclass, asdict


@dataclass
class SystemState:
    signal_attenuation_db: float = 0.0
    noise_attenuation_db: float = 0.0
    noise_enabled: bool = False
    doppler_shift_hz: float = 0.0
    measurement_point: str = "rf4"
    power_dbm: float = -20.0

    def to_dict(self) -> dict:
        return asdict(self)
