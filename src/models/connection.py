from dataclasses import dataclass


@dataclass
class Connection:
    from_hub: str
    to_hub: str
    max_link_capacity: int | None
