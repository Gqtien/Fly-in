from ursina import Color
from .drone import Drone
from .zone import ZoneType


class Hub:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        type: ZoneType,
        color: Color,
        max_drones: int | None = None,
    ):
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.type: ZoneType = type
        self.color: Color = color
        self.max_drones: int | None = max_drones
        self.drones: list[Drone] = []

    def has_capacity(self) -> bool:
        return self.max_drones is None or len(self.drones) < self.max_drones

    def add_drone(self, drone: Drone) -> bool:
        if (
            self.max_drones is None or len(self.drones) + 1 <= self.max_drones
        ) and drone not in self.drones:
            self.drones.append(drone)
            return True
        return False

    def remove_drone(self, drone: Drone) -> bool:
        if drone in self.drones:
            self.drones.remove(drone)
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.name} (drones: {len(self.drones)}/"
            f"{self.max_drones if self.max_drones is not None else '∞'})"
        )
