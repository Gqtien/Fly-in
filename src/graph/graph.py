from models import MapData
from collections import defaultdict

GraphType = dict[str, list[tuple[str, float]]]


class GraphBuilder:
    @staticmethod
    def build(data: MapData) -> GraphType:
        graph: GraphType = defaultdict(list)

        for conn in data.connections:
            graph[conn.from_hub].append(
                (conn.to_hub, data.hubs[conn.to_hub].type.value)
            )

        return dict(graph)
