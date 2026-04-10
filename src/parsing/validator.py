import os
from models import Connection, Hub, MapData


class Validator:
    def validate(self, data: MapData) -> None:
        self.validate_start_end(data)
        self.validate_hubs(data.hubs)
        self.validate_connections(data.hubs, data.connections)

    @staticmethod
    def validate_start_end(data: MapData) -> None:
        if data.start_hub not in data.hubs:
            raise ValueError("start_hub does not exist")
        if data.end_hub not in data.hubs:
            raise ValueError("end_hub does not exist")

    @staticmethod
    def validate_hubs(hubs: dict[str, Hub]) -> None:
        seen_coords = {}

        for name, hub in hubs.items():
            coord = (hub.x, hub.y)

            if coord in seen_coords:
                raise ValueError(
                    f"Duplicate coordinates {coord} for hubs "
                    f"'{seen_coords[coord]}' and '{name}'"
                )

            seen_coords[coord] = name

        for hub in hubs.values():
            if hub.max_drones is not None and hub.max_drones < 0:
                raise ValueError(f"Invalid max_drones for hub {hub.name}")

    @staticmethod
    def validate_connections(
        hubs: dict[str, Hub],
        connections: list[Connection]
    ) -> None:
        valid_hubs = set(hubs.keys())
        seen = set()

        for conn in connections:
            if conn.from_hub not in valid_hubs or conn.to_hub not in valid_hubs:
                raise ValueError(f"Invalid connection (unknown hub): {conn}")

            if conn.from_hub == conn.to_hub:
                continue

            key = (conn.from_hub, conn.to_hub)

            if key in seen:
                continue

            seen.add(key)

        for conn in connections:
            if conn.max_link_capacity is not None and conn.max_link_capacity <= 0:
                raise ValueError(f"Invalid capacity in connection {conn}")

    @staticmethod
    def validate_file_path(file_path: str) -> None:
        if file_path == "" or file_path == ():
            raise FileNotFoundError("No file selected")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Not a file: {file_path}")
        if not file_path.endswith(".txt"):
            raise FileNotFoundError(f"Not a .txt file: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise FileNotFoundError(f"File not readable: {file_path}")
