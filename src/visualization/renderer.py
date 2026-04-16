import arcade
from arcade import shape_list as sl
from models import Hub, MapData
from .config import BG_COLOR, HUB_RADIUS, ZONE_COLORS, ZOOM_FACTOR


class Renderer(arcade.View):
    def __init__(self, data: MapData, movements: list[list[str]]):
        super().__init__()
        self.data = data
        self.movements = movements
        self.total = len(movements)
        self.dragging = False
        self.scale = HUB_RADIUS * 1.5
        self.shape_list: sl.ShapeElementList = sl.ShapeElementList()
        self.text_cache: list[arcade.Text] = []
        self.invalidated: bool = True

    def on_show_view(self) -> None:
        self.camera = arcade.camera.Camera2D()
        hubs = list(self.data.hubs.values())
        self.camera.position = (
            (min(h.x for h in hubs) + max(h.x for h in hubs)) / 2 * self.scale,
            (min(h.y for h in hubs) + max(h.y for h in hubs)) / 2 * self.scale,
        )

    def _pos(self, hub: Hub) -> tuple[float, float]:
        return hub.x * self.scale, hub.y * self.scale

    def invalidate(self) -> None:
        self.invalidated = True

    def _rebuild_buffers(self) -> None:
        self.shape_list = sl.ShapeElementList()
        self.text_cache.clear()

        for conn in self.data.connections:
            hub_a = self.data.hubs[conn.from_hub]
            hub_b = self.data.hubs[conn.to_hub]
            ax, ay = self._pos(hub_a)
            bx, by = self._pos(hub_b)

            self.shape_list.append(
                sl.create_line(ax, ay, bx, by, arcade.color.WHITE, 4)
            )
            if len(conn.drones) > 0:
                self.text_cache.append(
                    arcade.Text(
                        str(conn.drones),
                        (ax + bx) / 2,
                        (ay + by) / 2,
                        arcade.color.WHITE,
                        font_size=HUB_RADIUS / 3,
                        anchor_x="center",
                        anchor_y="center",
                    )
                )

        for hub in self.data.hubs.values():
            x, y = self._pos(hub)
            clr, act = ZONE_COLORS.get(hub.type.name, ZONE_COLORS["NORMAL"])

            self.shape_list.append(
                sl.create_ellipse_filled(x, y, HUB_RADIUS, HUB_RADIUS, clr)
            )
            self.shape_list.append(
                sl.create_ellipse_outline(
                    x,
                    y,
                    HUB_RADIUS,
                    HUB_RADIUS,
                    hub.color,
                    HUB_RADIUS / 4,
                )
            )
            if len(hub.drones) > 0:
                self.text_cache.append(
                    arcade.Text(
                        str(len(hub.drones)),
                        x,
                        y,
                        act,
                        font_size=HUB_RADIUS / 3,
                        anchor_x="center",
                        anchor_y="center",
                    )
                )

        self.invalidated = False

    def on_draw(self) -> None:
        self.clear(BG_COLOR)
        if self.invalidated:
            self._rebuild_buffers()
        self.camera.use()
        self.shape_list.draw()
        for text in self.text_cache:
            text.draw()

    def on_mouse_press(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int,
    ) -> None:
        self.dragging = True

    def on_mouse_release(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int,
    ) -> None:
        self.dragging = False

    def on_mouse_drag(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
        buttons: int,
        modifiers: int,
    ) -> None:
        if self.dragging:
            cam_x, cam_y = self.camera.position
            self.camera.position = (cam_x - dx, cam_y - dy)

    def on_mouse_scroll(
        self,
        x: int,
        y: int,
        scroll_x: int,
        scroll_y: int,
    ) -> None:
        if scroll_y > 0:
            self.camera.zoom *= ZOOM_FACTOR
        elif scroll_y < 0:
            self.camera.zoom /= ZOOM_FACTOR
