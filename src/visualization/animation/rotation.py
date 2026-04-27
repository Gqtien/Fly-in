import math
from dataclasses import dataclass
from ..config import AnimationConfig


@dataclass(frozen=True)
class CarFrame:
    from_pos: tuple[float, float, float]
    to_pos: tuple[float, float, float]
    start_angle: float
    motion_angle: float
    next_angle: float | None


def ease_in_out(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)


def shortest_angle_diff(from_deg: float, to_deg: float) -> float:
    return ((to_deg - from_deg + 180.0) % 360.0) - 180.0


def interpolate_angle(from_deg: float, to_deg: float, t: float) -> float:
    return from_deg + shortest_angle_diff(from_deg, to_deg) * ease_in_out(t)


class RotationPhase:
    def __init__(self, start: float, end: float) -> None:
        self.start: float = start
        self.end: float = end

    def contains(self, t: float) -> bool:
        return self.start <= t < self.end

    def progress(self, t: float) -> float:
        span = self.end - self.start
        if span <= 0:
            return 1.0
        return (t - self.start) / span

    def angle(self, frame: CarFrame, t: float) -> float:
        raise NotImplementedError


class AlignmentPhase(RotationPhase):
    def angle(self, frame: CarFrame, t: float) -> float:
        return interpolate_angle(
            frame.start_angle, frame.motion_angle, self.progress(t)
        )


class CruisePhase(RotationPhase):
    def angle(self, frame: CarFrame, t: float) -> float:
        return frame.motion_angle


class ArrivalPhase(RotationPhase):
    def angle(self, frame: CarFrame, t: float) -> float:
        if frame.next_angle is None:
            return frame.motion_angle
        return interpolate_angle(
            frame.motion_angle, frame.next_angle, self.progress(t)
        )


class RotationTimeline:
    def __init__(self, config: AnimationConfig) -> None:
        self.phases: list[RotationPhase] = [
            AlignmentPhase(0.0, config.alignment_end),
            CruisePhase(config.alignment_end, config.arrival_start),
            ArrivalPhase(config.arrival_start, 1.0),
        ]

    def angle_at(self, t: float, frame: CarFrame) -> float:
        for phase in self.phases:
            if phase.contains(t):
                return phase.angle(frame, t)
        return frame.motion_angle
