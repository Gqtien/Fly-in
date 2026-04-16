import ursina as ur
from panda3d.core import CullFaceAttrib
from .utils import Utils


class Entity:
    @staticmethod
    def car(
        model: str,
        texture: str,
        pos: tuple[float, float, float] = (5, 0, 0),
        rot: tuple[float, float, float] = (0, 0, 0),
        scale: tuple[float, float, float] = (1.8, 1.8, 1.8),
    ) -> ur.Entity:
        car = ur.Entity(
            model=model,
            texture=texture,
            position=pos,
            rotation=rot,
            scale=scale,
        )
        for node in car.findAllMatches("**/+GeomNode"):
            node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
            return car

    @staticmethod
    def road(
        model: str,
        pos: tuple[float, float, float] = (0, 0, 0),
        rot: tuple[float, float, float] = (0, 0, 0),
        scale: tuple[float, float, float] = (1, 1, 1),
    ) -> ur.Entity:
        road = ur.Entity(
            model=model,
            texture="road_colorscheme.png",
            position=pos,
            rotation=rot,
            scale=scale,
        )
        for node in road.findAllMatches("**/+GeomNode"):
            node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
            return road

    @staticmethod
    def floor(texture: str = "grass.png") -> ur.Entity:
        floor = ur.Entity(
            model="plane",
            scale=50000,
            position=(0, -0.5, 0),
            texture=texture,
            texture_scale=(3000, 3000),
        )
        floor.setDepthOffset(1)
        return floor

    @staticmethod
    def sky(texture: str = "sky.png") -> ur.Entity:
        return ur.Sky(texture=texture)

    @staticmethod
    def hub(
        pos: tuple[float, float, float] = (0, 0, 0),
        color: ur.Color = ur.color.red,
    ) -> ur.Entity:
        x, y, z = pos
        pos = (x + 5, y - 0.1, z + 0.3)
        hub = ur.Entity(
            model=Utils().ring(),
            color=color,
            position=pos,
            rotation=(0, 0, 0),
            scale=(0.5, 0.5, 0.5),
        )
        hub.setDepthOffset(-1)
        for node in hub.findAllMatches("**/+GeomNode"):
            node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
            return hub
        return hub
