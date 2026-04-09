from typing import Any
from models import Connection, Hub, MapData, ZoneType


class Parser:
    def parse(self, path: str) -> MapData:
        with open(path, "r") as f:
            lines = f.readlines()
        lines = self._flatten(lines)
        return self._parse_entities(lines)

    @staticmethod
    def _flatten(lines: list[str]) -> list[str]:
        cleaned = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                cleaned.append(line)
        return cleaned

    def _parse_entities(self, lines: list[str]) -> MapData:
        nb_drones: int | None = None
        hubs: dict[str, Hub] = {}
        connections: list[Connection] = []
        start_hub: str | None = None
        end_hub: str | None = None

        for line in lines:
            try:
                parts: list[str] = line.split(":", 1)
                if parts[0] == "nb_drones":
                    nb_drones = int(parts[1].strip())
                elif parts[0] in ["hub", "start_hub", "end_hub"]:
                    hub = self._parse_hub(parts[1].strip())
                    hubs[hub.name] = hub
                    if parts[0] == "start_hub":
                        start_hub = hub.name
                    elif parts[0] == "end_hub":
                        end_hub = hub.name
                elif parts[0] == "connection":
                    connections.append(self._parse_connection(parts[1].strip()))
                else:
                    raise ValueError(f"Unknown entity type: {parts[0]}")
            except Exception as e:
                raise ValueError(f"Invalid line: {line}") from e

        if not nb_drones:
            raise ValueError("Missing nb_drones")
        if not hubs:
            raise ValueError("Missing hubs")
        if not start_hub:
            raise ValueError("Missing start_hub")
        if not end_hub:
            raise ValueError("Missing end_hub")

        return MapData(
            nb_drones=nb_drones,
            hubs=hubs,
            start_hub=start_hub,
            end_hub=end_hub,
            connections=connections,
        )

    def _parse_hub(self, data: str) -> Hub:
        parts = data.split(" ", 3)
        metadata = {}
        if len(parts) > 3:
            metadata = self._parse_metadata(parts[3])
        try:
            hub = Hub(
                name=parts[0].strip(),
                x=int(parts[1].strip()),
                y=int(parts[2].strip()),
                type=metadata.get("zone", ZoneType.NORMAL),
                color=metadata.get("color", None),
                max_drones = int(metadata["max_drones"]) if metadata.get("max_drones") is not None else None
            )
            if "-" in hub.name:
                raise ValueError(f"Invalid hub name: {hub.name}")
        except Exception as e:
            raise ValueError(f"Invalid hub data: {data}") from e
        return hub

    def _parse_connection(self, data: str) -> Connection:
        parts = data.split(" ", 2)
        metadata = {}
        if len(parts) > 1:
            metadata = self._parse_metadata(parts[1])
        try:
            return Connection(
                from_hub=parts[0].strip().split("-")[0],
                to_hub=parts[0].strip().split("-")[1],
                max_link_capacity=int(metadata["max_link_capacity"]) if metadata.get("max_link_capacity") is not None else None
            )
        except Exception as e:
            raise ValueError(f"Invalid connection data: {data}") from e

    @staticmethod
    def _parse_metadata(data: str) -> dict[str, Any]:
        if not data:
            return {}
        return {
            k: v for k, v in (item.split("=") for item in data.strip("[]").split(" "))
        }
