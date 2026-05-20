from dataclasses import dataclass
import ursina as ur


@dataclass(frozen=True)
class RoadConfig:
    asphalt_width: float = 8.0
    border_width: float = 1
    border_height: float = 0.7
    centerline_segments: int = 24
    pad_resolution: int = 48
    cell: float = 40.0
    asphalt_color: ur.Color = ur.color.dark_gray
    border_top_color: ur.Color = ur.color.light_gray
    border_bottom_color: ur.Color = ur.color.dark_gray
    hub_marker_height: float = 0.3
    hub_marker_radius_ratio: float = 0.5
    hub_marker_bottom_shade: float = 0.4
    stop_line_thickness: float = 1.0
    stop_line_lift: float = 0.05
    stop_line_dashes: int = 5
    stop_line_dash_ratio: float = 0.5
    stop_line_position: float = 0.53

    @property
    def half_asphalt(self) -> float:
        return self.asphalt_width / 2

    @property
    def pad_radius(self) -> float:
        return self.half_asphalt + self.border_width


@dataclass(frozen=True)
class CameraConfig:
    min_pitch: float = 1.0
    max_pitch: float = 89.0
    min_y: float = 1.0
    initial_pitch: float = 45.0
    initial_heading: float = 90.0
    framing_margin: float = 1.2


@dataclass(frozen=True)
class AnimationConfig:
    max_speed: float = 6.0
    step_duration: float = 0.6
    alignment_end: float = 0.15
    arrival_start: float = 0.75
    car_lift: float = 0.7


@dataclass(frozen=True)
class HudConfig:
    font: str = "noot.regular.ttf"
    scale: float = 1.0
    margin: float = 0.025
    color: ur.Color = ur.color.white


@dataclass(frozen=True)
class StackerConfig:
    font: str = "noot.regular.ttf"
    text_scale: float = 50.0
    text_color: ur.Color = ur.color.white
    plate_color: ur.Color = ur.color.black66
    plate_radius: float = 0.3
    plate_padding: tuple[float, float] = (0.03, 0.01)
    height_offset: float = 6
    cluster_eps: float = 0.05
    min_count: int = 2


@dataclass(frozen=True)
class TagConfig:
    font: str = "noot.regular.ttf"
    text_scale: float = 100.0
    text_color: ur.Color = ur.color.white
    accent_text_color: ur.Color = ur.color.light_gray
    shadow_color: ur.Color = ur.color.dark_gray
    shadow_offset: tuple[float, float] = (0.06, 0.06)
    height_offset: float = 1.05
    unlimited_text: str = ""
