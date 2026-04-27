import math
import ursina as ur
from models import Hub, HubGeometry, RoadGeometry
from ..config import RoadConfig
from ..utils import Utils
from .buffer import MeshBuffer


class RoadMeshBuilder:
    def __init__(self) -> None:
        self.config: RoadConfig = RoadConfig()

    def build_hub(self, hub: Hub) -> HubGeometry:
        return HubGeometry(
            asphalt=self.build_pad_disc(),
            border=self.build_pad_slab(),
            marker=self.build_hub_marker(hub.color),
            position=Utils.hub_world_pos(hub),
        )

    def build_pad_disc(self) -> ur.Mesh:
        n = self.config.pad_resolution
        r = self.config.half_asphalt
        h = self.config.border_height
        buffer = MeshBuffer()
        apex = buffer.add_apex(ur.Vec3(0, h, 0))
        ring = buffer.add_ring(n, r, h)
        buffer.add_fan(apex, ring, n)
        return buffer.to_mesh()

    def build_pad_slab(self) -> ur.Mesh:
        n = self.config.pad_resolution
        r = self.config.pad_radius
        h = self.config.border_height
        top = self.config.border_top_color
        bot = self.config.border_bottom_color
        buffer = MeshBuffer()
        apex = buffer.add_apex(ur.Vec3(0, h, 0), color=top)
        top_ring = buffer.add_ring(n, r, h, color=top)
        bot_ring = buffer.add_ring(n, r, 0, color=bot)
        buffer.add_fan(apex, top_ring, n)
        buffer.add_sides(top_ring, bot_ring, n)
        return buffer.to_mesh()

    def build_hub_marker(self, color: ur.Color) -> ur.Mesh:
        n = self.config.pad_resolution
        r = self.config.half_asphalt * self.config.hub_marker_radius_ratio
        h_bot = self.config.border_height
        h_top = h_bot + self.config.hub_marker_height
        bot_color = self.shade(color, self.config.hub_marker_bottom_shade)
        buffer = MeshBuffer()
        apex = buffer.add_apex(ur.Vec3(0, h_top, 0), color=color)
        top_ring = buffer.add_ring(n, r, h_top, color=color)
        bot_ring = buffer.add_ring(n, r, h_bot, color=bot_color)
        buffer.add_fan(apex, top_ring, n)
        buffer.add_sides(top_ring, bot_ring, n)
        return buffer.to_mesh()

    def build_road(self, a: Hub, b: Hub) -> RoadGeometry:
        a_world = ur.Vec3(*Utils.hub_world_pos(a))
        b_world = ur.Vec3(*Utils.hub_world_pos(b))
        handle = (b_world - a_world) / 3.0
        return self.extrude_ribbon(
            a_world, a_world + handle, b_world - handle, b_world
        )

    def extrude_ribbon(
        self, p0: ur.Vec3, p1: ur.Vec3, p2: ur.Vec3, p3: ur.Vec3
    ) -> RoadGeometry:
        n = self.config.centerline_segments
        ha = self.config.half_asphalt
        ht = self.config.pad_radius
        up = ur.Vec3(0, self.config.border_height, 0)
        top = self.config.border_top_color
        bot = self.config.border_bottom_color
        asphalt = MeshBuffer()
        border = MeshBuffer()
        for i in range(n + 1):
            t = i / n
            c = self.bezier(p0, p1, p2, p3, t)
            r = self.normalised(
                self.right_of(self.bezier_tangent(p0, p1, p2, p3, t))
            )
            asphalt.vertices += [c + r * ha + up, c - r * ha + up]
            border.vertices += [
                c + r * ht,
                c + r * ht + up,
                c - r * ht + up,
                c - r * ht,
            ]
            border.colors += [bot, top, top, bot]
            if i > 0:
                base_a = (i - 1) * 2
                asphalt.triangles += [
                    (base_a, base_a + 1, base_a + 3),
                    (base_a, base_a + 3, base_a + 2),
                ]
                base_b = (i - 1) * 4
                border.triangles += self.slab_quads(base_b)
        return RoadGeometry(
            asphalt=asphalt.to_mesh(),
            borders=border.to_mesh(),
        )

    @staticmethod
    def slab_quads(base: int) -> list[tuple[int, int, int]]:
        rb, rt, lt, lb = base, base + 1, base + 2, base + 3
        rb_n, rt_n, lt_n, lb_n = base + 4, base + 5, base + 6, base + 7
        return [
            (rt, rt_n, lt_n),
            (rt, lt_n, lt),
            (rb, rb_n, rt_n),
            (rb, rt_n, rt),
            (lb_n, lb, lt),
            (lb_n, lt, lt_n),
        ]

    @staticmethod
    def shade(color: ur.Color, factor: float) -> ur.Color:
        return ur.Color(
            color[0] * factor,
            color[1] * factor,
            color[2] * factor,
            color[3],
        )

    @staticmethod
    def bezier(
        p0: ur.Vec3,
        p1: ur.Vec3,
        p2: ur.Vec3,
        p3: ur.Vec3,
        t: float,
    ) -> ur.Vec3:
        u = 1.0 - t
        return (
            (u * u * u) * p0
            + (3 * u * u * t) * p1
            + (3 * u * t * t) * p2
            + (t * t * t) * p3
        )

    @staticmethod
    def bezier_tangent(
        p0: ur.Vec3,
        p1: ur.Vec3,
        p2: ur.Vec3,
        p3: ur.Vec3,
        t: float,
    ) -> ur.Vec3:
        u = 1.0 - t
        return (
            (3 * u * u) * (p1 - p0) + (6 * u * t)
            * (p2 - p1) + (3 * t * t) * (p3 - p2)
        )

    @staticmethod
    def normalised(v: ur.Vec3) -> ur.Vec3:
        n = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
        return v / n if n > 0 else ur.Vec3(0, 0, 0)

    @staticmethod
    def right_of(tangent: ur.Vec3) -> ur.Vec3:
        return ur.Vec3(tangent.z, 0.0, -tangent.x)
