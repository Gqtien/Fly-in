from collections import deque
from models import MapData, ZoneType
from ..errors import MapError


class GraphValidator:
    def validate(self, data: MapData) -> None:
        self.check_endpoints(data)
        self.check_blocked_endpoints(data)
        self.check_unique_coordinates(data)
        self.check_connection_endpoints(data)
        self.check_reachability(data)

    @staticmethod
    def check_endpoints(data: MapData) -> None:
        if data.start_hub not in data.hubs:
            raise MapError(f"start_hub '{data.start_hub}' is not declared")
        if data.end_hub not in data.hubs:
            raise MapError(f"end_hub '{data.end_hub}' is not declared")
        if data.start_hub == data.end_hub:
            raise MapError("start_hub and end_hub must be different")

    @staticmethod
    def check_blocked_endpoints(data: MapData) -> None:
        if data.hubs[data.start_hub].type == ZoneType.BLOCKED:
            raise MapError("start_hub cannot be a blocked zone")
        if data.hubs[data.end_hub].type == ZoneType.BLOCKED:
            raise MapError("end_hub cannot be a blocked zone")

    @staticmethod
    def check_unique_coordinates(data: MapData) -> None:
        seen: dict[tuple[int, int], str] = {}
        for hub in data.hubs.values():
            coord = (hub.x, hub.y)
            if coord in seen:
                raise MapError(
                    f"hubs '{seen[coord]}' and '{hub.name}' "
                    f"share coordinates {coord}"
                )
            seen[coord] = hub.name

    @staticmethod
    def check_connection_endpoints(data: MapData) -> None:
        names = set(data.hubs)
        for conn in data.connections:
            if conn.from_hub not in names:
                raise MapError(
                    f"connection references unknown hub '{conn.from_hub}'"
                )
            if conn.to_hub not in names:
                raise MapError(
                    f"connection references unknown hub '{conn.to_hub}'"
                )

    def check_reachability(self, data: MapData) -> None:
        neighbors = self.build_neighbor_map(data)
        blocked = self.blocked_set(data)
        reachable = self.reachable_from(data.start_hub, neighbors, blocked)
        if data.end_hub not in reachable:
            raise MapError(
                f"end_hub '{data.end_hub}' is unreachable from "
                f"start_hub '{data.start_hub}'"
            )
        unreachable = set(data.hubs) - reachable - blocked
        if unreachable:
            sample = sorted(unreachable)[0]
            raise MapError(
                f"hub '{sample}' is disconnected from start_hub"
            )

    @staticmethod
    def build_neighbor_map(data: MapData) -> dict[str, set[str]]:
        neighbors: dict[str, set[str]] = {name: set() for name in data.hubs}
        for conn in data.connections:
            neighbors[conn.from_hub].add(conn.to_hub)
            neighbors[conn.to_hub].add(conn.from_hub)
        return neighbors

    @staticmethod
    def blocked_set(data: MapData) -> set[str]:
        return {
            name for name, hub in data.hubs.items()
            if hub.type == ZoneType.BLOCKED
        }

    @staticmethod
    def reachable_from(
        start: str,
        neighbors: dict[str, set[str]],
        blocked: set[str],
    ) -> set[str]:
        seen: set[str] = {start}
        queue: deque[str] = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in neighbors[node]:
                if neighbor in blocked or neighbor in seen:
                    continue
                seen.add(neighbor)
                queue.append(neighbor)
        return seen
