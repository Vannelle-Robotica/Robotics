import enum


class OperatingMode(enum.Enum):
    controlled = 0
    autonomous = 1
    lineDance = 2
    dancing = 3

    def next(self):
        value = self.value
        if value == 3:
            return OperatingMode.controlled
        return OperatingMode(value + 1)
