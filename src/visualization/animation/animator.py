import math
import ursina as ur
from models import MapData
from ..config import AnimationConfig
from .playback import PlaybackState
from .rotation import CarFrame, RotationTimeline, ease_in_out
from .trajectory import Trajectory


class Animator(ur.Entity):
    def __init__(
        self,
        data: MapData,
        movements: list[list[str]],
        cars: dict[int, ur.Entity],
    ) -> None:
        super().__init__()
        self.data: MapData = data
        self.movements: list[list[str]] = movements
        self.cars: dict[int, ur.Entity] = cars
        self.config: AnimationConfig = AnimationConfig()
        self.trajectory: Trajectory = Trajectory(
            data, movements, list(cars.keys()), self.config
        )
        self.timeline: RotationTimeline = RotationTimeline(self.config)
        self.state: PlaybackState = PlaybackState(len(movements))
        self.frames: dict[int, CarFrame] = {}
        self.chain_in: bool = False
        self.chain_out: bool = False
        self.snap_to(0)

    def update(self) -> None:
        if self.state.is_animating:
            prev_direction = self.state.direction
            crossed = self.state.tick(ur.time.dt, self.config.step_duration)
            if crossed:
                self.snap_to(self.state.current_step)
                if (
                    self.state.consume_chain()
                    and self.can_step(prev_direction)
                ):
                    self.start_animation(prev_direction, chain_in=True)
                else:
                    self.state.reset_chain()
            else:
                self.apply_frames(self.state.elapsed)
            return
        if self.state.autoplay and self.state.can_step_forward():
            self.start_animation(1)

    def can_step(self, direction: int) -> bool:
        if direction > 0:
            return self.state.can_step_forward()
        if direction < 0:
            return self.state.can_step_backward()
        return False

    def toggle_autoplay(self) -> None:
        self.state.toggle_autoplay()

    def step_forward(self) -> None:
        self.state.pause()
        if self.state.is_animating and self.state.direction > 0:
            self.state.queue_chain()
            return
        self.state.reset_chain()
        self.state.complete()
        if self.state.can_step_forward():
            self.start_animation(1)
        else:
            self.snap_to(self.state.current_step)

    def step_backward(self) -> None:
        self.state.pause()
        if self.state.is_animating and self.state.direction < 0:
            self.state.queue_chain()
            return
        self.state.reset_chain()
        self.state.complete()
        if self.state.can_step_backward():
            self.start_animation(-1)
        else:
            self.snap_to(self.state.current_step)

    def restart(self) -> None:
        self.state.restart()
        self.snap_to(0)

    def start_animation(
        self, direction: int, *, chain_in: bool = False
    ) -> None:
        self.chain_in = chain_in
        self.chain_out = self.state.queue > 0
        self.state.start(direction)
        self.capture_frames(direction)
        self.apply_frames(0.0)

    def capture_frames(self, direction: int) -> None:
        self.frames = {}
        from_state = self.trajectory.state_at(self.state.current_step)
        to_state = self.trajectory.state_at(
            self.state.current_step + direction
        )
        for drone_id, car in self.cars.items():
            frame = self.build_frame(
                drone_id, car, from_state, to_state, direction
            )
            if frame is not None:
                self.frames[drone_id] = frame

    def build_frame(
        self,
        drone_id: int,
        car: ur.Entity,
        from_state: dict[int, str],
        to_state: dict[int, str],
        direction: int,
    ) -> CarFrame | None:
        from_pos = from_state.get(drone_id)
        to_pos = to_state.get(drone_id)
        if from_pos is None or to_pos is None or from_pos == to_pos:
            return None
        from_world = self.trajectory.world_at(from_pos)
        to_world = self.trajectory.world_at(to_pos)
        start_angle = car.rotation_y
        return CarFrame(
            from_pos=self.trajectory.car_world(from_world),
            to_pos=self.trajectory.car_world(to_world),
            start_angle=start_angle,
            motion_angle=self.motion_angle_for(
                start_angle, from_world, to_world, direction
            ),
            next_angle=self.lookahead_angle(
                drone_id, to_pos, to_world, direction
            ),
        )

    def motion_angle_for(
        self,
        start_angle: float,
        from_world: tuple[float, float, float],
        to_world: tuple[float, float, float],
        direction: int,
    ) -> float:
        if direction > 0:
            return self.heading(from_world, to_world)
        return start_angle

    def lookahead_angle(
        self,
        drone_id: int,
        to_pos: str,
        to_world: tuple[float, float, float],
        direction: int,
    ) -> float | None:
        if direction <= 0:
            return None
        next_target = self.trajectory.next_motion_target(
            drone_id, self.state.current_step + direction, to_pos
        )
        if next_target is None:
            return None
        next_world = self.trajectory.world_at(next_target)
        return self.heading(to_world, next_world)

    def apply_frames(self, t: float) -> None:
        trans_eased = self.translation_ease(t)
        for drone_id, frame in self.frames.items():
            car = self.cars[drone_id]
            car.x = (
                frame.from_pos[0]
                + (frame.to_pos[0] - frame.from_pos[0])
                * trans_eased
            )
            car.y = frame.from_pos[1]
            car.z = (
                frame.from_pos[2]
                + (frame.to_pos[2] - frame.from_pos[2])
                * trans_eased
            )
            car.rotation_y = self.timeline.angle_at(t, frame)

    def translation_ease(self, t: float) -> float:
        if self.chain_in and self.chain_out:
            return t
        if self.chain_in:
            return -(t ** 3) + (t ** 2) + t
        if self.chain_out:
            return 2 * (t ** 2) - (t ** 3)
        return ease_in_out(t)

    def snap_to(self, step: int) -> None:
        state = self.trajectory.state_at(step)
        for drone_id, pos in state.items():
            car = self.cars.get(drone_id)
            if car is None:
                continue
            world = self.trajectory.world_at(pos)
            cw = self.trajectory.car_world(world)
            car.x, car.y, car.z = cw
            next_target = self.trajectory.next_motion_target(
                drone_id, step, pos
            )
            if next_target is not None:
                next_world = self.trajectory.world_at(next_target)
                car.rotation_y = self.heading(world, next_world)

    @staticmethod
    def heading(
        from_world: tuple[float, float, float],
        to_world: tuple[float, float, float],
    ) -> float:
        dx = to_world[0] - from_world[0]
        dz = to_world[2] - from_world[2]
        return math.degrees(math.atan2(dx, dz))
