from ..config import AnimationConfig


class PlaybackState:
    def __init__(self, total_steps: int) -> None:
        self.total_steps: int = total_steps
        self.current_step: int = 0
        self.elapsed: float = 0.0
        self.direction: int = 0
        self.autoplay: bool = True
        self.queue: int = 0
        self.speed_factor: float = 1.0

    @property
    def is_animating(self) -> bool:
        return self.direction != 0

    def can_step_forward(self) -> bool:
        return self.current_step < self.total_steps

    def can_step_backward(self) -> bool:
        return self.current_step > 0

    def start(self, direction: int) -> None:
        self.direction = direction
        self.elapsed = 0.0

    def tick(self, dt: float, step_duration: float) -> bool:
        if not self.is_animating:
            return False
        self.elapsed += dt * self.speed_factor / step_duration
        if self.elapsed >= 1.0:
            self.complete()
            return True
        return False

    def complete(self) -> int:
        if self.is_animating:
            self.current_step += self.direction
            self.elapsed = 0.0
            self.direction = 0
        return self.current_step

    def queue_chain(self) -> None:
        self.queue += 1
        self.speed_factor = min(1.0 + self.queue, AnimationConfig.max_speed)

    def consume_chain(self) -> bool:
        if self.queue > 0:
            self.queue -= 1
            return True
        self.speed_factor = 1.0
        return False

    def reset_chain(self) -> None:
        self.queue = 0
        self.speed_factor = 1.0

    def toggle_autoplay(self) -> None:
        self.autoplay = not self.autoplay

    def pause(self) -> None:
        self.autoplay = False

    def restart(self) -> None:
        self.current_step = 0
        self.elapsed = 0.0
        self.direction = 0
        self.autoplay = True
        self.reset_chain()
