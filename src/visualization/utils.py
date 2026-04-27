from models import Hub
from .config import RoadConfig


class Utils:
    @staticmethod
    def hub_world_pos(hub: Hub) -> tuple[float, float, float]:
        return (hub.y * RoadConfig.cell, 0.0, -hub.x * RoadConfig.cell)
