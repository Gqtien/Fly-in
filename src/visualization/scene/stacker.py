import ursina as ur
from panda3d.core import CullFaceAttrib, DepthTestAttrib
from ..config import StackerConfig


class StackTag(ur.Entity):
    def __init__(self, config: StackerConfig) -> None:
        super().__init__(parent=ur.scene, enabled=False)
        self.config: StackerConfig = config
        self.plate: ur.Entity = ur.Entity(
            parent=self,
            color=config.plate_color,
        )
        self.plate.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.plate.setAttrib(DepthTestAttrib.make(DepthTestAttrib.M_none))
        self.plate.setBin("fixed", 10)
        self.label: ur.Text = ur.Text(
            parent=self,
            text="",
            font=config.font,
            origin=(0, 0),
            scale=config.text_scale,
            color=config.text_color,
        )
        self.label.setAttrib(DepthTestAttrib.make(DepthTestAttrib.M_none))
        self.label.setBin("fixed", 20)
        self.count: int = 0

    def show(
        self,
        position: tuple[float, float, float],
        count: int,
    ) -> None:
        self.enabled = True
        self.position = position
        if count != self.count:
            self.count = count
            self.label.text = f"x{count}"
            pad_x, pad_y = self.config.plate_padding
            scale = self.config.text_scale
            self.plate.scale_x = (self.label.width + pad_x) * scale
            self.plate.scale_y = (self.label.height + pad_y) * scale
            self.plate.model = ur.Quad(
                radius=self.config.plate_radius,
                aspect=self.plate.scale_x / self.plate.scale_y,
            )

    def hide(self) -> None:
        self.enabled = False

    def update(self) -> None:
        self.look_at(ur.camera, axis=ur.Vec3.back)
        self.rotation_z = 0


class Stacker(ur.Entity):
    def __init__(self, cars: dict[int, ur.Entity]) -> None:
        super().__init__()
        self.cars: dict[int, ur.Entity] = cars
        self.config: StackerConfig = StackerConfig()
        self.pool: list[StackTag] = []

    def update(self) -> None:
        clusters = self.cluster_cars()
        active = 0
        for cluster in clusters.values():
            if len(cluster) < self.config.min_count:
                continue
            self.acquire(active).show(
                self.anchor(cluster), len(cluster)
            )
            active += 1
        for tag in self.pool[active:]:
            tag.hide()

    def cluster_cars(
        self,
    ) -> dict[tuple[int, int, int], list[ur.Entity]]:
        eps = self.config.cluster_eps
        clusters: dict[tuple[int, int, int], list[ur.Entity]] = {}
        for car in self.cars.values():
            key = (
                round(car.x / eps),
                round(car.y / eps),
                round(car.z / eps),
            )
            clusters.setdefault(key, []).append(car)
        return clusters

    def anchor(
        self, cluster: list[ur.Entity]
    ) -> tuple[float, float, float]:
        n = len(cluster)
        cx = sum(c.x for c in cluster) / n
        cz = sum(c.z for c in cluster) / n
        cy = max(c.y for c in cluster) + self.config.height_offset
        return (cx, cy, cz)

    def acquire(self, index: int) -> StackTag:
        while index >= len(self.pool):
            self.pool.append(StackTag(self.config))
        return self.pool[index]
