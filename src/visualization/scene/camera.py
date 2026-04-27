import math
import ursina as ur
from models import MapData
from ..config import CameraConfig
from ..utils import Utils


class Camera(ur.EditorCamera):
    y: float

    def __init__(
        self,
        target: tuple[float, float, float] = (0.0, 0.0, 0.0),
        distance: float = 50.0,
    ) -> None:
        super().__init__()
        self.target: tuple[float, float, float] = target
        self.distance: float = distance
        self.config: CameraConfig = CameraConfig()
        self.reset()

    @classmethod
    def for_map(cls, data: MapData) -> "Camera":
        start = data.hubs.get(data.start_hub)
        end = data.hubs.get(data.end_hub)
        if start is None or end is None:
            return cls()
        sp = Utils.hub_world_pos(start)
        ep = Utils.hub_world_pos(end)
        cx = (sp[0] + ep[0]) / 2
        cz = (sp[2] + ep[2]) / 2
        span = math.hypot(ep[0] - sp[0], ep[2] - sp[2])
        hfov_rad = math.radians(ur.camera.fov)
        distance = (
            (span * CameraConfig.framing_margin / 2)
            / math.tan(hfov_rad / 2)
        )
        return cls((cx, 0.0, cz), max(distance, 50.0))

    def on_enable(self) -> None:
        super().on_enable()
        if hasattr(self, "target"):
            self.reset()

    def reset(self) -> None:
        self.position = self.target
        self.rotation_x = self.config.initial_pitch
        self.rotation_y = self.config.initial_heading
        ur.camera.position = (0, 0, -self.distance)
        self.target_z = -self.distance

    def update(self) -> None:
        super().update()
        pitch = self.rotation_x
        self.rotation_x = max(
            self.config.min_pitch,
            min(self.config.max_pitch, pitch)
        )
        height: float = self.y
        if height < self.config.min_y:
            self.y = self.config.min_y
