from dataclasses import dataclass


Entry = tuple[int, dict[str, str]]


@dataclass(frozen=True)
class LexResult:
    nb_drones: int
    start_hub: Entry
    end_hub: Entry
    hubs: list[Entry]
    connections: list[Entry]
