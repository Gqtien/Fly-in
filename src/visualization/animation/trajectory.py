from models import MapData
from ..config import AnimationConfig
from ..utils import Utils


class Trajectory:
    def __init__(
        self,
        data: MapData,
        movements: list[list[str]],
        drone_ids: list[int],
        config: AnimationConfig,
    ) -> None:
        self.data: MapData = data
        self.movements: list[list[str]] = movements
        self.config: AnimationConfig = config
        self.positions: list[dict[int, str]] = self.compute_positions(
            drone_ids
        )

    def compute_positions(
        self, drone_ids: list[int]
    ) -> list[dict[int, str]]:
        initial: dict[int, str] = {
            drone_id: self.data.start_hub for drone_id in drone_ids
        }
        positions: list[dict[int, str]] = [initial]
        for step in self.movements:
            current = dict(positions[-1])
            for entry in step:
                head, _, pos = entry.partition("-")
                if not pos:
                    continue
                drone_id = int(head[1:])
                if drone_id in current:
                    current[drone_id] = pos
            positions.append(current)
        return positions

    def state_at(self, step: int) -> dict[int, str]:
        return self.positions[step]

    def world_at(self, position: str) -> tuple[float, float, float]:
        if "-" in position:
            a, b = position.split("-", 1)
            pa = Utils.hub_world_pos(self.data.hubs[a])
            pb = Utils.hub_world_pos(self.data.hubs[b])
            return (
                (pa[0] + pb[0]) / 2,
                (pa[1] + pb[1]) / 2,
                (pa[2] + pb[2]) / 2,
            )
        return Utils.hub_world_pos(self.data.hubs[position])

    def next_motion_target(
        self, drone_id: int, from_step: int, base_pos: str
    ) -> str | None:
        for step in range(from_step + 1, len(self.positions)):
            pos = self.positions[step].get(drone_id)
            if pos is not None and pos != base_pos:
                return pos
        return None

    def car_world(
        self,
        world: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        return (
            world[0],
            world[1] + self.config.car_lift,
            world[2] + self.config.car_z_offset,
        )
