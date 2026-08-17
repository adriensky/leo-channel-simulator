from gpiozero import LED
import threading
import time


class StatusLED:
    def __init__(self, pin: int = 5):
        self.led = LED(pin)
        self._blink_thread = None
        self._running = False

    def on(self):
        self._stop_blink()
        self.led.on()

    def off(self):
        self._stop_blink()
        self.led.off()

    def blink(self, interval: float):
        self._stop_blink()
        self._running = True

        def _loop():
            while self._running:
                self.led.toggle()
                time.sleep(interval)

        self._blink_thread = threading.Thread(target=_loop, daemon=True)
        self._blink_thread.start()

    def _stop_blink(self):
        self._running = False
        if self._blink_thread:
            self._blink_thread.join(timeout=0.1)
            self._blink_thread = None

    def startup(self):
        self.blink(1.0)  # 1 Hz

    def error(self):
        self.blink(0.2)  # rapide

    def ready(self):
        self.on()
