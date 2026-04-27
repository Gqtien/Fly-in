from pathlib import Path
import ursina as ur
from models import MapData
from .animation import Animator
from .mesh import RoadMeshBuilder
from .scene import Camera, Controller, Entity, Hud
from .utils import Utils


class Renderer:
    def __init__(
        self,
        data: MapData,
        movements: list[list[str]],
        debug: bool = False,
    ) -> None:
        self.data: MapData = data
        self.movements: list[list[str]] = movements
        self.total_turns: int = len(movements)
        self.debug: bool = debug

        self.setup()
        self.render()
        Controller(self.camera, self.animator)
        self.app.run()

    def setup(self) -> None:
        root = Path(__file__).parent.parent.parent / "assets"
        ur.application.asset_folder = root
        ur.application.development_mode = self.debug
        self.app: ur.Ursina = ur.Ursina(title="Fly-In", fullscreen=True)
        ur.application.base.camLens.setNearFar(1, 9e10)
        self.camera: Camera = Camera.for_map(self.data)
        self.entity: Entity = Entity()
        self.entity.floor()
        self.entity.sky()

    def render(self) -> None:
        self.spawn_roads()
        self.spawn_cars()
        self.animator: Animator = Animator(
            self.data,
            self.movements,
            self.cars,
        )
        Hud(self.animator)

    def spawn_roads(self) -> None:
        builder = RoadMeshBuilder()
        for hub in self.data.hubs.values():
            hub_geom = builder.build_hub(hub)
            self.entity.border(hub_geom.border, hub_geom.position)
            self.entity.asphalt(hub_geom.asphalt, hub_geom.position)
            self.entity.marker(hub_geom.marker, hub_geom.position)
        for c in self.data.connections:
            road_geom = builder.build_road(
                self.data.hubs[c.from_hub], self.data.hubs[c.to_hub]
            )
            self.entity.border(road_geom.borders)
            self.entity.asphalt(road_geom.asphalt)

    def spawn_cars(self) -> None:
        self.cars: dict[int, ur.Entity] = {}
        for drone in self.data.hubs[self.data.start_hub].drones:
            car = self.entity.car(
                model="taxi.dae",
                texture="taxi_texture.jpg",
                pos=Utils.hub_world_pos(self.data.hubs[drone.position]),
            )
            self.cars[drone.id] = car
