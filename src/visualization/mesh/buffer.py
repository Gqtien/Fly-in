import math
from dataclasses import dataclass, field
import ursina as ur


@dataclass
class MeshBuffer:
    vertices: list[ur.Vec3] = field(default_factory=list)
    triangles: list[tuple[int, int, int]] = field(default_factory=list)
    colors: list[ur.Color] = field(default_factory=list)

    def add_apex(
        self, pos: ur.Vec3, color: ur.Color | None = None
    ) -> int:
        index = len(self.vertices)
        self.vertices.append(pos)
        if color is not None:
            self.colors.append(color)
        return index

    def add_ring(
        self,
        n: int,
        radius: float,
        y: float,
        color: ur.Color | None = None,
    ) -> int:
        start = len(self.vertices)
        for i in range(n):
            a = math.tau * i / n
            self.vertices.append(
                ur.Vec3(math.cos(a) * radius, y, math.sin(a) * radius)
            )
            if color is not None:
                self.colors.append(color)
        return start

    def add_fan(self, apex: int, ring_start: int, n: int) -> None:
        self.triangles += [
            (apex, ring_start + i, ring_start + (i + 1) % n)
            for i in range(n)
        ]

    def add_sides(
        self, top_start: int, bot_start: int, n: int
    ) -> None:
        for i in range(n):
            j = (i + 1) % n
            top0, top1 = top_start + i, top_start + j
            bot0, bot1 = bot_start + i, bot_start + j
            self.triangles += [
                (bot0, top0, top1),
                (bot0, top1, bot1),
            ]

    def to_mesh(self) -> ur.Mesh:
        if self.colors:
            return ur.Mesh(
                vertices=self.vertices,
                triangles=self.triangles,
                colors=self.colors,
                mode="triangle",
            )
        return ur.Mesh(
            vertices=self.vertices,
            triangles=self.triangles,
            mode="triangle",
        )
