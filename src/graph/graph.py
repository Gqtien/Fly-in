from models import MapData, ZoneType
from collections import defaultdict

GraphType = dict[str, list[tuple[str, float]]]


class GraphBuilder:
    @staticmethod
    def build(data: MapData) -> GraphType:
        graph: GraphType = defaultdict(list)

        for conn in data.connections:
            to_hub = data.hubs[conn.to_hub]
            from_hub = data.hubs[conn.from_hub]

            if to_hub.type is not ZoneType.BLOCKED:
                graph[conn.from_hub].append(
                    (conn.to_hub, to_hub.type.weight)
                )
            if from_hub.type is not ZoneType.BLOCKED:
                graph[conn.to_hub].append(
                    (conn.from_hub, from_hub.type.weight)
                )

        return dict(graph)
