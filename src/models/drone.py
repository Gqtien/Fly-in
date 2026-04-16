from dataclasses import dataclass, field
from enum import Enum


class DroneStatus(Enum):
    IDLE = "idle"
    TRANSITING = "transiting"
    ON_CONNECTION = "on_connection"


@dataclass
class Drone:
    id: int
    position: str
    status: DroneStatus = DroneStatus.IDLE
    path: list[str] = field(default_factory=list)
