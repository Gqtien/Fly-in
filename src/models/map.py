from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    model_validator,
)
from .connection import Connection
from .drone import Drone
from .hub import Hub, HubName
from .limits import Limits


class MapData(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    nb_drones: PositiveInt
    start_hub: HubName
    end_hub: HubName
    hubs: dict[str, Hub]
    connections: list[Connection]
    drones: list[Drone] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_limits(self) -> "MapData":
        if self.nb_drones > Limits.max_nb_drones:
            raise ValueError(
                f"nb_drones exceeds {Limits.max_nb_drones}"
            )
        if len(self.hubs) > Limits.max_hubs:
            raise ValueError(f"hub count exceeds {Limits.max_hubs}")
        if len(self.connections) > Limits.max_connections:
            raise ValueError(
                f"connection count exceeds {Limits.max_connections}"
            )
        return self
