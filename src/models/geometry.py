from dataclasses import dataclass
from ursina import Mesh


@dataclass(frozen=True)
class HubGeometry:
    asphalt: Mesh
    border: Mesh
    marker: Mesh
    position: tuple[float, float, float]


@dataclass(frozen=True)
class RoadGeometry:
    asphalt: Mesh
    borders: Mesh
