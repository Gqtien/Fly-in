from models import MapData, Hub
from graph import Graph, GraphType
from typing import TypeAlias

PathType: TypeAlias = tuple[float, list[str]]


class Djikstra:
    def __init__(self, data: MapData) -> None:
        self.data: MapData = data
        self.graph: GraphType = Graph().map_to_graph(self.data)

    def find_path(self) -> PathType:
        stack: list[Hub] = []
        visited: list[Hub] = []
        start: Hub = self.data.hubs[self.data.start_hub]
        stack.append(start)
        visited.append(start)

        while stack:
            current: Hub = stack[-1]
            neighbors: list[str] = self.graph.get(current.name, [])
            unvisited: list[Hub] = [
                self.data.hubs[n] for n in neighbors if n not in visited
            ]

        if unvisited:
            neighbor: Hub = unvisited[0]
            # forward drone
            visited.append(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()

        return 0.0, []
