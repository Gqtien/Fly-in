from dataclasses import dataclass
from .zone import ZoneType
from arcade.types import Color


@dataclass
class Hub:
    name: str
    x: int
    y: int
    type: ZoneType
    color: Color
    max_drones: int | None
