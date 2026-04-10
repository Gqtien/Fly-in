import arcade

from models import MapData
from .config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from .renderer import Renderer


class Viewer:
    def __init__(self, data: MapData) -> None:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        renderer = Renderer(data)

        window.show_view(renderer)
        arcade.run()
