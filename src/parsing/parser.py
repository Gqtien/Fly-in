from typing import Any, cast
import arcade
from arcade.types import Color
from models import Connection, Hub, MapData, ZoneType
from .validator import Validator


class Parser:
    def parse(self, path: str) -> MapData:
        with open(path, "r") as f:
            lines = f.readlines()
        lines = self._flatten(lines)
        data = self._parse_entities(lines)
        Validator().validate(data)
        return data

    @staticmethod
    def _flatten(lines: list[str]) -> list[str]:
        flat = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                flat.append(stripped)
        return flat

    def _parse_entities(self, lines: list[str]) -> MapData:
        nb_drones: int | None = None
        hubs: dict[str, Hub] = {}
        connections: list[Connection] = []
        start_hub: str | None = None
        end_hub: str | None = None

        for line in lines:
            try:
                key, value = line.split(":", 1)
                value = value.strip()

                if key == "nb_drones":
                    nb_drones = int(value)

                elif key in ["hub", "start_hub", "end_hub"]:
                    hub = self._parse_hub(value)
                    hubs[hub.name] = hub
                    if key == "start_hub":
                        start_hub = hub.name
                    if key == "end_hub":
                        end_hub = hub.name

                elif key == "connection":
                    connections.append(self._parse_connection(value))
                else:
                    raise ValueError(f"Unknown entity type: {key}")
            except Exception as e:
                raise ValueError(f"Invalid line: {line}") from e

        if nb_drones is None:
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
        name, x, y = parts[:3]
        metadata = self._parse_metadata(parts[3]) if len(parts) > 3 else {}
        try:
            if "-" in name:
                raise ValueError(f"Invalid hub name: {name}")

            hub = Hub(
                name=name,
                x=int(x),
                y=int(y),
                type=self._parse_zone_t(metadata.get("zone")),
                color=self._parse_color(metadata.get("color")),
                max_drones=self._to_int(metadata.get("max_drones")),
            )
        except Exception as e:
            raise ValueError(f"Invalid hub data: {data}") from e
        return hub

    def _parse_connection(self, data: str) -> Connection:
        parts = data.split(" ", 2)
        hubs_part = parts[0].strip()
        meta = self._parse_metadata(parts[1]) if len(parts) > 1 else {}
        try:
            from_hub, to_hub = hubs_part.split("-")
            return Connection(
                from_hub=from_hub,
                to_hub=to_hub,
                max_link_capacity=self._to_int(meta.get("max_link_capacity")),
            )
        except Exception as e:
            raise ValueError(f"Invalid connection data: {data}") from e

    @staticmethod
    def _parse_metadata(data: str) -> dict[str, Any]:
        if not data:
            return {}

        return dict(
            item.split("=", 1)
            for item in data.strip("[]").split()
            if "=" in item
        )

    @staticmethod
    def _to_int(value: str | None) -> int | None:
        return int(value) if value else None

    @staticmethod
    def _parse_color(name: str | None) -> Color:
        if not name:
            return arcade.color.WHITE
        try:
            return cast(Color, getattr(arcade.color, name.upper()))
        except AttributeError:
            return arcade.color.WHITE

    @staticmethod
    def _parse_zone_t(name: str | None) -> ZoneType:
        if not name:
            return ZoneType.NORMAL
        try:
            return ZoneType[name.upper()]
        except KeyError:
            return ZoneType.NORMAL
