import ursina as ur
from panda3d.core import CullFaceAttrib, DepthTestAttrib
from ..config import RoadConfig


class LiftedSurface(ur.Entity):
    def __init__(
        self,
        mesh: ur.Mesh,
        pos: tuple[float, float, float],
        color: ur.Color,
    ) -> None:
        super().__init__(model=mesh, color=color, position=pos)
        self.setAttrib(DepthTestAttrib.make(DepthTestAttrib.M_less_equal))
        for node in self.findAllMatches("**/+GeomNode"):
            node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.base_y: float = pos[1]
        self.y = self.base_y

    def update(self) -> None:
        d = ur.camera.world_position.length()
        lift = max(0, d * d / 4e6)
        self.y = self.base_y + lift


class Entity:
    @staticmethod
    def car(
        model: str,
        texture: str,
        pos: tuple[float, float, float] = (0, 0, 0),
        rot: tuple[float, float, float] = (0, 0, 0),
        scale: tuple[float, float, float] = (2, 2, 2),
    ) -> ur.Entity:
        x, y, z = pos
        pos = (x, y + 0.7, z - 1)
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
    def asphalt(
        mesh: ur.Mesh,
        pos: tuple[float, float, float] = (0, 0, 0),
    ) -> ur.Entity:
        return LiftedSurface(mesh, pos, RoadConfig.asphalt_color)

    @staticmethod
    def marker(
        mesh: ur.Mesh,
        pos: tuple[float, float, float] = (0, 0, 0),
    ) -> ur.Entity:
        return LiftedSurface(mesh, pos, ur.color.white)

    @staticmethod
    def border(
        mesh: ur.Mesh,
        pos: tuple[float, float, float] = (0, 0, 0),
    ) -> ur.Entity:
        border = ur.Entity(
            model=mesh,
            color=ur.color.white,
            position=pos,
        )
        for node in border.findAllMatches("**/+GeomNode"):
            node.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        return border

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
