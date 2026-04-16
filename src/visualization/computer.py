from models import MapData, Road, RoadType


class Computer:
    def __init__(self, data: MapData) -> None:
        self.data = data

    def compute_roads_pos(self) -> dict[RoadType, Road]:
        roads: dict[RoadType, Road] = {}
        default: RoadType = ((0, 0, 0), (0, 0, 0), (1, 1, 1))
        roads[default] = Road.END
        for _, hub in self.data.hubs.items():
            ...
        return roads

    def compute_camera_pos(self) -> tuple[float, float, float]:
        return (10, 10, 10)
