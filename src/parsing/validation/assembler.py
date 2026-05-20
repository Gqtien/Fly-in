from typing import Any, TypeVar
from pydantic import BaseModel, ValidationError
from models import Connection, Drone, Hub, MapData
from ..errors import MapError
from ..lex import Entry, LexResult


ModelT = TypeVar("ModelT", bound=BaseModel)


class Assembler:
    def assemble(self, result: LexResult) -> MapData:
        start = self.build_hub(*result.start_hub)
        end = self.build_hub(*result.end_hub)
        start.is_endpoint = True
        end.is_endpoint = True
        hubs = self.build_hubs(result.hubs, [start, end])
        connections = self.build_connections(result.connections)
        drones = [
            Drone(id=i, position=start.name)
            for i in range(result.nb_drones)
        ]
        for drone in drones:
            hubs[start.name].add_drone(drone)
        return self.validate_or_raise(MapData, {
            "nb_drones": result.nb_drones,
            "start_hub": start.name,
            "end_hub": end.name,
            "hubs": hubs,
            "connections": connections,
            "drones": drones,
        })

    def build_hub(self, line_no: int, fields: dict[str, str]) -> Hub:
        return self.validate_or_raise(Hub, fields, line_no)

    def build_hubs(
        self,
        entries: list[Entry],
        endpoints: list[Hub],
    ) -> dict[str, Hub]:
        hubs: dict[str, Hub] = {}
        for hub in endpoints:
            if hub.name in hubs:
                raise MapError(
                    f"start_hub and end_hub share the same name '{hub.name}'"
                )
            hubs[hub.name] = hub
        for line_no, fields in entries:
            hub = self.build_hub(line_no, fields)
            if hub.name in hubs:
                raise MapError(
                    f"duplicate hub name '{hub.name}'",
                    line_no,
                )
            hubs[hub.name] = hub
        return hubs

    def build_connections(
        self,
        entries: list[Entry],
    ) -> list[Connection]:
        seen: set[frozenset[str]] = set()
        connections: list[Connection] = []

        for line_no, fields in entries:
            conn = self.validate_or_raise(Connection, fields, line_no)
            key = frozenset({conn.from_hub, conn.to_hub})
            if key in seen:
                raise MapError(
                    f"duplicate connection between '{conn.from_hub}' "
                    f"and '{conn.to_hub}'",
                    line_no,
                )
            seen.add(key)
            connections.append(conn)
        return connections

    def validate_or_raise(
        self,
        model: type[ModelT],
        fields: dict[str, Any],
        line_no: int | None = None,
    ) -> ModelT:
        try:
            return model.model_validate(fields)
        except ValidationError as e:
            raise MapError(self.format_error(e), line_no) from e

    @staticmethod
    def format_error(error: ValidationError) -> str:
        first = error.errors()[0]
        loc = ".".join(str(p) for p in first["loc"]) or "value"
        return f"{loc}: {first['msg']}"
