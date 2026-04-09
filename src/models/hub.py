from dataclasses import dataclass
from .color import Color
from .zone import ZoneType


@dataclass
class Hub:
    name: str
    x: int
    y: int
    type: ZoneType
    color: Color | None
    max_drones: int | None
