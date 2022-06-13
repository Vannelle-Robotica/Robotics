import enum


class OperatingMode(enum.Enum):
    autonomous = 0
    controlled = 1
    lineDance = 2
    dancing = 3

    def next(self):
        value = self.value
        if value == OperatingMode.dancing:
            return OperatingMode.autonomous
        return OperatingMode(value + 1)