import arcade
from .renderer import Renderer
from .config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from models import MapData


class Viewer:
    def __init__(self, data: MapData) -> None:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        renderer = Renderer(data)

        window.show_view(renderer)
        arcade.run()
