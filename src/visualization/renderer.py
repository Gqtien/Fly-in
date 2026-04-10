import arcade
from models import MapData, Hub
from .config import HUB_RADIUS, ZONE_COLORS, ZOOM_FACTOR, BG_COLOR


class Renderer(arcade.View):
    def __init__(self, data: MapData):
        super().__init__()
        self.data = data

        self.dragging = False
        self.scale = HUB_RADIUS * 3

    def on_show_view(self) -> None:
        self.camera = arcade.camera.Camera2D()

        hubs = list(self.data.hubs.values())

        min_x = min(h.x for h in hubs)
        max_x = max(h.x for h in hubs)
        min_y = min(h.y for h in hubs)
        max_y = max(h.y for h in hubs)

        self.camera.position = (
            (min_x + max_x) / 2 * self.scale,
            (min_y + max_y) / 2 * self.scale,
        )

    def _pos(self, hub: Hub) -> tuple[float, float]:
        return hub.x * self.scale, hub.y * self.scale

    def on_draw(self) -> None:
        self.clear(BG_COLOR)
        self.camera.use()

        for conn in self.data.connections:
            hub_a = self.data.hubs[conn.from_hub]
            hub_b = self.data.hubs[conn.to_hub]

            ax, ay = self._pos(hub_a)
            bx, by = self._pos(hub_b)

            arcade.draw_line(ax, ay, bx, by, arcade.color.WHITE, 4)

        for hub in self.data.hubs.values():
            x, y = self._pos(hub)

            clr = ZONE_COLORS.get(hub.type.name, ZONE_COLORS["NORMAL"])["MAIN"]

            arcade.draw_circle_filled(x, y, HUB_RADIUS, clr)
            arcade.draw_circle_outline(x, y, HUB_RADIUS, hub.color, 3)

    def on_mouse_press(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int
    ) -> None:
        self.dragging = True

    def on_mouse_release(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int
    ) -> None:
        self.dragging = False

    def on_mouse_drag(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
        buttons: int,
        modifiers: int
    ) -> None:
        if not self.dragging:
            return

        cam_x, cam_y = self.camera.position
        self.camera.position = (cam_x - dx, cam_y - dy)

    def on_mouse_scroll(
        self,
        x: int,
        y: int,
        scroll_x: int,
        scroll_y: int
    ) -> None:
        if scroll_y > 0:
            self.camera.zoom *= ZOOM_FACTOR
        elif scroll_y < 0:
            self.camera.zoom /= ZOOM_FACTOR
