import ursina as ur
from pathlib import Path
from models import MapData, Road, RoadType
from .entity import Entity
from .computer import Computer
from .controller import Controller


class Renderer:
    def __init__(
        self, data: MapData, movements: list[list[str]], debug: bool = False
    ) -> None:
        self.data: MapData = data
        self.movements: list[list[str]] = movements
        self.total_turns: int = len(movements)
        self.debug: bool = debug

        self.computer: Computer = Computer(data)

        self.setup()
        self.render()
        Controller(data)
        self.app.run()

    def setup(self) -> None:
        root = Path(__file__).parent.parent.parent / "assets"
        ur.application.asset_folder = root
        ur.application.development_mode = self.debug
        self.app: ur.Ursina = ur.Ursina(title="Fly-In", fullscreen=True)
        ur.application.base.camLens.setNearFar(1, 9e10)
        ur.EditorCamera()
        self.entity: Entity = Entity()
        self.entity.floor()
        self.entity.sky()

    def render(self) -> None:
        self.spawn_roads()
        self.spawn_cars()
        self.spawn_hubs()
        self.spawn_labels()

    def spawn_roads(self) -> None:
        roads: dict[RoadType, Road] = self.computer.compute_roads_pos()
        for place, type in roads.items():
            pos, rot = place
            self.entity.road(type.value, pos, rot)

    def spawn_cars(self) -> None:
        self.cars: dict[int, ur.Entity] = {}
        for drone in self.data.hubs[self.data.start_hub].drones:
            car = self.entity.car(
                model="taxi.dae",
                texture="taxi_texture.jpg",
                pos=(
                    self.data.hubs[drone.position].y * 20,
                    0,
                    -(self.data.hubs[drone.position].x * 20 + 5),
                ),
                scale=(1.8, 1.8, 1.8),
            )
            self.cars[drone.id] = car

    def spawn_hubs(self) -> None:
        for _, hub in self.data.hubs.items():
            self.entity.hub(
                pos=(hub.y * 20, 0, -(hub.x * 20)),
                color=hub.color,
            )

    def spawn_labels(self) -> None:
        label = ur.Text(
            text=f"{self.total_turns} turns",
            parent=ur.camera.ui,
            origin=(0.5, 0.5),
            scale=0.75,
            font="Satoshi-Medium.otf",
        )

        label.x = round(-ur.window.aspect_ratio / 2 + label.width / 2, 3)
        label.y = round(0.48, 3)
