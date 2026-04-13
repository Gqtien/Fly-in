from models import MapData
from typing import TypeAlias
from collections import defaultdict

GraphType: TypeAlias = dict[str, list[str]]


class Graph:
    @staticmethod
    def map_to_graph(data: MapData) -> GraphType:
        graph: defaultdict[str, list[str]] = defaultdict(list)

        for conn in data.connections:
            graph[conn.from_hub].append(conn.to_hub)

        return dict(graph)
