from dataclasses import dataclass
from .connection import Connection
from .hub import Hub


@dataclass
class MapData:
    nb_drones: int
    start_hub: str
    end_hub: str
    hubs: dict[str, Hub]
    connections: list[Connection]
