import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Fly-In"

HUB_RADIUS = 25
ZOOM_FACTOR = 1.1

BG_COLOR = arcade.color.QUARTZ

ZONE_COLORS = {
    "NORMAL": (arcade.color.WHITE, arcade.color.BLACK),
    "PRIORITY": (arcade.color.GREEN, arcade.color.WHITE),
    "RESTRICTED": (arcade.color.RED, arcade.color.WHITE),
    "BLOCKED": (arcade.color.BLACK, arcade.color.WHITE),
}
