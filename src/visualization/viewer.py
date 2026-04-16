import arcade

from models import MapData
from .config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from .renderer import Renderer


class Viewer:
    def __init__(self, data: MapData, movements: list[list[str]]) -> None:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        renderer = Renderer(data, movements)

        window.show_view(renderer)
        arcade.run()
