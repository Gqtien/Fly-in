from graph import GraphBuilder, GraphType
from models import Drone, DroneStatus, MapData, Connection, ZoneType
from .scheduler import Scheduler
import copy


class Simulator:
    def __init__(self, data: MapData) -> None:
        self.data: MapData = copy.deepcopy(data)
        self.graph: GraphType = GraphBuilder.build(self.data)
        self.scheduler: Scheduler = Scheduler(self.graph)

    def simulate(self) -> list[list[str]]:
        movements: list[list[str]] = []

        with open("out.txt", "w") as f:
            while not self.is_done():
                movements.append(self.step())
                f.write(" ".join(movements[-1]) + "\n")

            f.write(f"\nTotal turns: {len(movements)}\n")

        return movements

    def step(self) -> list[str]:
        idle_count = sum(
            1
            for d in self.data.drones
            if d.status == DroneStatus.IDLE
            and d.position != self.data.end_hub
        )
        self.scheduler.assign(
            self.data.drones,
            [self.data.end_hub] * idle_count,
        )

        movements: list[str] = []
        for drone in self.data.drones:
            if drone.status == DroneStatus.ON_CONNECTION or (
                drone.status == DroneStatus.TRANSITING and len(drone.path) > 1
            ):
                if self.advance(drone):
                    movements.append(f"D{drone.id}-{drone.position}")

        return movements

    def is_done(self) -> bool:
        return all(d.position == self.data.end_hub for d in self.data.drones)

    def advance(self, drone: Drone) -> bool:
        if drone.status == DroneStatus.ON_CONNECTION:
            from_hub, to_hub = drone.position.split("-")
            conn = self.get_connection(from_hub, to_hub)
            if conn:
                conn.remove_drone(drone)
            self.data.hubs[to_hub].add_drone(drone)
            drone.position = to_hub
            drone.status = (
                DroneStatus.TRANSITING
                if len(drone.path) > 1
                else DroneStatus.IDLE
            )
            return True

        from_hub = drone.path[0]
        to_hub = drone.path[1]

        if self.data.hubs[to_hub].type is ZoneType.RESTRICTED:
            conn = self.get_connection(from_hub, to_hub)
            if conn and not conn.has_capacity():
                return False
            drone.path.pop(0)
            self.data.hubs[from_hub].remove_drone(drone)
            if conn:
                conn.add_drone(drone)
            drone.position = f"{from_hub}-{to_hub}"
            drone.status = DroneStatus.ON_CONNECTION
        else:
            if not self.data.hubs[to_hub].has_capacity():
                return False
            drone.path.pop(0)
            self.data.hubs[from_hub].remove_drone(drone)
            self.data.hubs[to_hub].add_drone(drone)
            drone.position = to_hub
            drone.status = (
                DroneStatus.TRANSITING
                if len(drone.path) > 1
                else DroneStatus.IDLE
            )
        return True

    def get_connection(self, from_hub: str, to_hub: str) -> Connection | None:
        for conn in self.data.connections:
            if {conn.from_hub, conn.to_hub} == {from_hub, to_hub}:
                return conn
        return None
