from enum import Enum


class ZoneType(Enum):
    BLOCKED = 0
    RESTRICTED = 1
    NORMAL = 2
    PRIORITY = 3

    @property
    def weight(self) -> int:
        return self.value

    @staticmethod
    def from_str(value: str) -> "ZoneType":
        return ZoneType[value.upper()]
