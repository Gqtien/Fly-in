from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    max_file_size: int = 1 * 1024 * 1024
    max_line_len: int = 1024
    max_hubs: int = 10_000
    max_connections: int = 50_000
    max_nb_drones: int = 10_000
    max_name_len: int = 64
    hub_name_pattern: str = r"^[A-Za-z_][A-Za-z0-9_]*$"
    color_pattern: str = r"^[A-Za-z][A-Za-z0-9_]*$"
    allowed_hub_keys: frozenset[str] = frozenset(
        {"zone", "color", "max_drones"}
    )
    allowed_connection_keys: frozenset[str] = frozenset(
        {"max_link_capacity"}
    )
