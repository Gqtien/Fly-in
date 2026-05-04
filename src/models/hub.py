import re
from typing import Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    StringConstraints,
    field_validator,
)
from ursina import Color, color as ur_color
from .drone import Drone
from .limits import Limits
from .zone import ZoneType


HubName = Annotated[
    str,
    StringConstraints(
        pattern=Limits.hub_name_pattern,
        max_length=Limits.max_name_len,
    ),
]


class Hub(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        populate_by_name=True,
    )

    name: HubName
    x: int
    y: int
    type: ZoneType = Field(default=ZoneType.NORMAL, alias="zone")
    color: Color = Field(default_factory=lambda: ur_color.white)
    max_drones: PositiveInt | None = None
    drones: list[Drone] = Field(default_factory=list)

    @field_validator("color", mode="before")
    @classmethod
    def coerce_color(cls, v: object) -> Color:
        if isinstance(v, Color):
            return v
        if v is None:
            return ur_color.white
        if not isinstance(v, str):
            raise ValueError(
                f"color must be string or Color, got {type(v).__name__}"
            )
        if not re.match(Limits.color_pattern, v):
            raise ValueError(f"invalid color name: '{v}'")
        return getattr(ur_color, v.lower(), ur_color.white)

    def has_capacity(self) -> bool:
        return (
            self.max_drones is None
            or len(self.drones) < self.max_drones
        )

    def add_drone(self, drone: Drone) -> bool:
        if (
            self.max_drones is None
            or len(self.drones) + 1 <= self.max_drones
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
        cap = self.max_drones if self.max_drones is not None else "∞"
        return f"{self.name} (drones: {len(self.drones)}/{cap})"
