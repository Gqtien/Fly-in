from graph import GraphType
from pathfinding import Dijkstra, DijkstraType
from models import Drone, DroneStatus


class Scheduler:
    def __init__(self, graph: GraphType) -> None:
        self.graph: GraphType = graph
        self.dijkstra: Dijkstra = Dijkstra(self.graph)

    def assign(self, drones: list[Drone], tasks: list[str]) -> list[str]:
        available = [d for d in drones if d.status == DroneStatus.IDLE]

        pos_cache: dict[str, DijkstraType] = {}
        for d in available:
            if d.position not in pos_cache:
                pos_cache[d.position] = self.dijkstra.run(d.position)

        assignments: list[str] = []
        for task in tasks:
            best_drone = None
            best_cost = float("inf")
            best_path: list[str] = []

            for drone in available:
                dist, prev = pos_cache[drone.position]
                cost = dist.get(task, float("inf"))
                if cost < best_cost:
                    best_cost = cost
                    best_drone = drone
                    best_path = self.dijkstra.reconstruct(
                        prev, drone.position, task
                    )

            if best_drone and len(best_path) > 1:
                best_drone.path = best_path
                best_drone.status = DroneStatus.TRANSITING
                assignments.append(str(best_drone.id))
                available.remove(best_drone)

        return assignments
