from gpiozero import OutputDevice


class RFSwitchDriver:
    def __init__(
        self,
        v1_pin: int = 22,
        v2_pin: int = 23,
        v3_pin: int = 24,
    ) -> None:
        self._v1 = OutputDevice(v1_pin, active_high=True, initial_value=False)
        self._v2 = OutputDevice(v2_pin, active_high=True, initial_value=False)
        self._v3 = OutputDevice(v3_pin, active_high=True, initial_value=False)

    def _apply(self, v1: bool, v2: bool, v3: bool) -> None:
        if v1:
            self._v1.on()
        else:
            self._v1.off()

        if v2:
            self._v2.on()
        else:
            self._v2.off()

        if v3:
            self._v3.on()
        else:
            self._v3.off()

    def select_rf1(self) -> dict:
        # State 2: V3 Low, V2 Low, V1 High
        self._apply(v1=True, v2=False, v3=False)
        return self.status("RF1")

    def select_rf2(self) -> dict:
        # State 3: V3 Low, V2 High, V1 Low
        self._apply(v1=False, v2=True, v3=False)
        return self.status("RF2")

    def select_rf3(self) -> dict:
        # State 4: V3 Low, V2 High, V1 High
        self._apply(v1=True, v2=True, v3=False)
        return self.status("RF3")

    def select_rf4(self) -> dict:
        # Prefer State 1: V3 Low, V2 Low, V1 Low
        self._apply(v1=False, v2=False, v3=False)
        return self.status("RF4")

    def all_off(self) -> dict:
        # State 6: V3 High, V2 Low, V1 High
        self._apply(v1=True, v2=False, v3=True)
        return self.status("ALL_OFF")

    def status(self, selected: str | None = None) -> dict:
        v1 = bool(self._v1.value)
        v2 = bool(self._v2.value)
        v3 = bool(self._v3.value)

        if selected is None:
            if (v1, v2, v3) == (False, False, False):
                selected = "RF4"
            elif (v1, v2, v3) == (True, False, False):
                selected = "RF1"
            elif (v1, v2, v3) == (False, True, False):
                selected = "RF2"
            elif (v1, v2, v3) == (True, True, False):
                selected = "RF3"
            elif (v1, v2, v3) in [(True, False, True), (False, True, True)]:
                selected = "ALL_OFF"
            else:
                selected = "UNSUPPORTED"

        return {
            "selected": selected,
            "v1": v1,
            "v2": v2,
            "v3": v3,
        }

    def cleanup(self) -> None:
        self._v1.off()
        self._v2.off()
        self._v3.off()
        self._v1.close()
        self._v2.close()
        self._v3.close()
