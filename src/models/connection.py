from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    model_validator,
)
from .drone import Drone
from .hub import HubName


class Connection(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        populate_by_name=True,
    )

    from_hub: HubName = Field(alias="a")
    to_hub: HubName = Field(alias="b")
    max_link_capacity: PositiveInt = 1
    drones: list[Drone] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_self_loop(self) -> "Connection":
        if self.from_hub == self.to_hub:
            raise ValueError(
                f"connection cannot loop on '{self.from_hub}'"
            )
        return self

    def has_capacity(self) -> bool:
        return len(self.drones) < self.max_link_capacity

    def add_drone(self, drone: Drone) -> bool:
        if drone in self.drones:
            return False
        if len(self.drones) >= self.max_link_capacity:
            return False
        self.drones.append(drone)
        return True

    def remove_drone(self, drone: Drone) -> bool:
        if drone in self.drones:
            self.drones.remove(drone)
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.from_hub} -> {self.to_hub} "
            f"(drones: {len(self.drones)}/{self.max_link_capacity})"
        )
