from enum import Enum
from typing import TypeAlias

Coordinate: TypeAlias = tuple[float, float, float]
RoadType: TypeAlias = tuple[Coordinate, Coordinate]


class Road(Enum):
    STRAIGHT = "road_straight.dae"
    CURVE = "road_curve.dae"
    S_CURVE = "road_s-curve.dae"
    END = "road_end.dae"
    JOIN = "road_join.dae"
    CROSS = "road_cross.dae"
