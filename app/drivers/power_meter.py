import hid
import logging

logger = logging.getLogger(__name__)

VENDOR_ID  = 0x20CE
PRODUCT_ID = 0x11
BUF_SIZE   = 64

# Interrupt command codes (section 3.2 of Mini-Circuits PWR Series programming manual)
CMD_GET_MODEL  = 104
CMD_GET_SERIAL = 105
CMD_SET_MODE   = 15
CMD_READ_POWER = 102
CMD_GET_TEMP   = 103
CMD_GET_FW     = 99
CMD_SEND_SCPI  = 42   # RC series only; response starts at byte 8

# Measurement modes for set_measurement_mode()
MODE_LOW_NOISE = 0
MODE_FAST      = 1
MODE_FASTEST   = 2  # PWR-8FS only

# Sample time limits (µs) for set_sample_time_us()
SAMPLE_TIME_MIN_US = 10
SAMPLE_TIME_MAX_US = 1_000_000  # 1 second


class PowerMeterDriver:
    """Driver for Mini-Circuits PWR Series USB power sensors (Linux HID).

    Requires libhidapi on the host:
        sudo apt install libhidapi-hidraw0
    """

    def __init__(self):
        self._dev = hid.Device(vid=VENDOR_ID, pid=PRODUCT_ID)
        self._dev.nonblocking = False
        logger.info("Power meter connected: %s (SN %s)", self.get_model(), self.get_serial())

    def close(self) -> None:
        self._dev.close()

    # ------------------------------------------------------------------ helpers

    def _send(self, payload: list) -> list:
        """Send a 64-byte HID packet and return the 64-byte response."""
        # hidapi requires a leading report-ID byte (0x00 for devices without report IDs)
        buf = [0x00] + payload + [0x00] * (BUF_SIZE - len(payload))
        self._dev.write(bytes(buf[:BUF_SIZE + 1]))
        return self._dev.read(BUF_SIZE, timeout=1000)

    @staticmethod
    def _ascii_string(resp: list, start: int = 1) -> str:
        """Decode a null-terminated ASCII string from a response buffer.

        Stops at 0x00 (null terminator) or any non-printable/non-ASCII byte
        (e.g. 0xFF 'don't care' bytes returned by some firmware builds).
        """
        chars = []
        for b in resp[start:]:
            if b == 0 or b > 0x7E:
                break
            chars.append(chr(b))
        return "".join(chars)

    # ------------------------------------------------------------------ info

    def get_model(self) -> str:
        """Return the Mini-Circuits part number (e.g. 'PWR-8FS')."""
        return self._ascii_string(self._send([CMD_GET_MODEL]))

    def get_serial(self) -> str:
        """Return the device serial number."""
        return self._ascii_string(self._send([CMD_GET_SERIAL]))

    def get_firmware(self) -> str:
        """Return the firmware revision identifier (e.g. 'C3')."""
        resp = self._send([CMD_GET_FW])
        return chr(resp[3]) + chr(resp[4])

    # ------------------------------------------------------------------ control

    def set_measurement_mode(self, mode: int = MODE_LOW_NOISE) -> None:
        """Set measurement mode: MODE_LOW_NOISE (0), MODE_FAST (1), MODE_FASTEST (2)."""
        self._send([CMD_SET_MODE, mode])

    # ------------------------------------------------------------------ measurements

    def read_power_dbm(self, freq_mhz: float = 1000.0) -> float:
        """Read the current power level in dBm.

        Args:
            freq_mhz: Compensation frequency in MHz. Defaults to 1000 MHz.

        Returns:
            Power reading in dBm.
        """
        freq_int = int(freq_mhz)
        freq_1   = freq_int // 256
        freq_2   = freq_int - freq_1 * 256
        # Byte 3: 77 = ord('M') selects MHz units
        resp = self._send([CMD_READ_POWER, freq_1, freq_2, 77])
        # Response bytes 1–6 are ASCII chars, format "+00.00" (null-terminated)
        return float(self._ascii_string(resp, start=1))

    def get_temperature_c(self) -> float:
        """Return the internal sensor temperature in degrees Celsius."""
        resp = self._send([CMD_GET_TEMP])
        return float(self._ascii_string(resp, start=1))

    # ------------------------------------------------------------------ SCPI (RC series)

    def send_scpi(self, command: str) -> str:
        """Send a raw SCPI command string and return the response string.

        The response payload starts at byte 8 of the returned buffer (bytes 1-7
        are reserved) and is null-terminated.  Only supported on RC series sensors.
        """
        payload = [CMD_SEND_SCPI] + [ord(c) for c in command]
        resp = self._send(payload)
        return self._ascii_string(resp, start=8)

    # ------------------------------------------------------------------ sample time

    def get_sample_time_us(self) -> int:
        """Return the current sample (integration) time in microseconds."""
        return int(self.send_scpi(":SAMPLETIME?"))

    def set_sample_time_us(self, time_us: int) -> None:
        """Set the sample (integration) time in microseconds (10 – 1,000,000 µs)."""
        self.send_scpi(f":SAMPLETIME:{time_us}")

    # ------------------------------------------------------------------ averaging

    def get_avg_mode(self) -> bool:
        """Return True if averaging mode is enabled."""
        return self.send_scpi(":AVG:STATE?").strip() == "1"

    def set_avg_mode(self, enabled: bool) -> None:
        """Enable or disable measurement averaging."""
        self.send_scpi(f":AVG:STATE:{1 if enabled else 0}")

    def get_avg_count(self) -> int:
        """Return the number of readings averaged per measurement (1–32)."""
        return int(self.send_scpi(":AVG:COUNT?"))

    def set_avg_count(self, count: int) -> None:
        """Set the number of readings averaged per measurement (1–32)."""
        self.send_scpi(f":AVG:COUNT:{count}")
