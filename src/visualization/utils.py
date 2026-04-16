import ursina as ur
import math


class Utils:
    @staticmethod
    def ring(
        resolution: int = 15,
        radius: int = 4,
        thickness: float = 1,
        height: float = 0.5,
    ) -> ur.Mesh:
        verts: list[ur.Vec3] = []
        tris: list[tuple[int, int, int]] = []
        for i in range(resolution):
            a0 = math.tau * i / resolution
            a1 = math.tau * (i + 1) / resolution
            r_in, r_out = radius - thickness, radius
            c0i = ur.Vec3(math.cos(a0) * r_in, 0, math.sin(a0) * r_in)
            c0o = ur.Vec3(math.cos(a0) * r_out, 0, math.sin(a0) * r_out)
            c1o = ur.Vec3(math.cos(a1) * r_out, 0, math.sin(a1) * r_out)
            c1i = ur.Vec3(math.cos(a1) * r_in, 0, math.sin(a1) * r_in)
            t0i = ur.Vec3(math.cos(a0) * r_in, height, math.sin(a0) * r_in)
            t0o = ur.Vec3(math.cos(a0) * r_out, height, math.sin(a0) * r_out)
            t1o = ur.Vec3(math.cos(a1) * r_out, height, math.sin(a1) * r_out)
            t1i = ur.Vec3(math.cos(a1) * r_in, height, math.sin(a1) * r_in)

            v = len(verts)
            verts += [c0i, c0o, c1o, c1i, t0i, t0o, t1o, t1i]
            tris += [(v, v + 1, v + 2), (v, v + 2, v + 3)]
            tris += [(v + 4, v + 6, v + 5), (v + 4, v + 7, v + 6)]
            tris += [(v + 1, v + 5, v + 6), (v + 1, v + 6, v + 2)]
            tris += [(v + 0, v + 3, v + 7), (v + 0, v + 7, v + 4)]

        return ur.Mesh(vertices=verts, triangles=tris, mode="triangle")
