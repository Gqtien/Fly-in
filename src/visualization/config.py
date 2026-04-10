import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Fly-In"

HUB_RADIUS = 25
ZOOM_FACTOR = 1.1

BG_COLOR = arcade.color.QUARTZ

ZONE_COLORS = {
    "NORMAL": {
        "MAIN": arcade.color.WHITE,
        "ACCENT": arcade.color.BLACK,
    },
    "PRIORITY": {
        "MAIN": arcade.color.GREEN,
        "ACCENT": arcade.color.WHITE,
    },
    "RESTRICTED": {
        "MAIN": arcade.color.RED,
        "ACCENT": arcade.color.WHITE,
    },
    "BLOCKED": {
        "MAIN": arcade.color.BLACK,
        "ACCENT": arcade.color.WHITE,
    },
}
