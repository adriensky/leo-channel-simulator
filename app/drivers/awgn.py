from gpiozero import OutputDevice
from app.config import settings


class NoiseGeneratorDriver:
    def __init__(self) -> None:
        self._ttl = OutputDevice(
            settings.noise_generator_ttl_pin,
            active_high=settings.noise_generator_active_high,
            initial_value=False,
        )

    def enable(self) -> None:
        print("NoiseGeneratorDriver: GPIO17 ON")
        self._ttl.on()

    def disable(self) -> None:
        print("NoiseGeneratorDriver: GPIO17 OFF")
        self._ttl.off()

    def status(self) -> dict:
        return {
            "enabled": bool(self._ttl.value),
            "pin": settings.noise_generator_ttl_pin,
        }

    def cleanup(self) -> None:
        self._ttl.off()
        self._ttl.close()
