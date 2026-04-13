from arcade.types import Color
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
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_drones = max_drones
        self.drones = 0

    def add_drone(self, amount: int = 1) -> bool:
        if self.max_drones is None or self.drones + amount <= self.max_drones:
            self.drones += amount
            return True
        return False

    def remove_drone(self) -> bool:
        if self.drones > 0:
            self.drones -= 1
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.name} (drones: {self.drones}/"
            f"{self.max_drones if self.max_drones is not None else '∞'})"
        )
