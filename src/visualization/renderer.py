import ursina as ur
from pathlib import Path
from models import MapData, Road, RoadType
from .entity import Entity
from .computer import Computer


class Renderer:
    def __init__(
        self, data: MapData, movements: list[list[str]], debug: bool = False
    ) -> None:
        self.data: MapData = data
        self.movements: list[list[str]] = movements
        self.debug: bool = debug

        self.computer: Computer = Computer(data)

        self.setup()
        self.render()
        self.app.run()

    def setup(self) -> None:
        root = Path(__file__).parent.parent.parent / "assets"
        ur.application.asset_folder = root
        ur.application.development_mode = self.debug
        self.app: ur.Ursina = ur.Ursina(title="Fly-In")
        ur.application.base.camLens.setNearFar(1, 10_000_000)
        ur.EditorCamera()
        self.entity: Entity = Entity()
        Entity.floor()
        Entity.sky()

    def render(self) -> None:
        self.spawn_roads()
        self.spawn_cars()
        self.spawn_hubs()

    def spawn_roads(self) -> None:
        roads: dict[RoadType, Road] = self.computer.compute_roads_pos()
        for place, type in roads.items():
            pos, rot, scale = place
            self.entity.road(type.value, pos, rot, scale)

    def spawn_cars(self) -> None:
        self.entity.car(
            model="taxi.dae",
            texture="taxi_texture.jpg",
            pos=(5, 0.01, 0),
            scale=(1.8, 1.8, 1.8),
        )

    def spawn_hubs(self) -> None:
        for _, hub in self.data.hubs.items():
            self.entity.hub(
                pos=(hub.y * 20, 0, -(hub.x * 20)),
                color=hub.color,
            )
