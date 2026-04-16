from enum import Enum


class ZoneType(Enum):
    BLOCKED = 0
    RESTRICTED = 1
    NORMAL = 2
    PRIORITY = 3

    @property
    def weight(self) -> float:
        weights: dict["ZoneType", float] = {
            ZoneType.BLOCKED: float("inf"),
            ZoneType.NORMAL: 1.0,
            ZoneType.RESTRICTED: 2.0,
            ZoneType.PRIORITY: 0.5,
        }
        return weights[self]

    @staticmethod
    def from_str(value: str) -> "ZoneType":
        return ZoneType[value.upper()]
