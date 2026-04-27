import ursina as ur
from ..animation import Animator
from ..config import HudConfig


class Hud(ur.Entity):
    def __init__(self, animator: Animator) -> None:
        super().__init__()
        self.animator: Animator = animator
        self.config: HudConfig = HudConfig()
        self.stats: ur.Text = self.build_stats()
        self.build_controls()
        self.refresh()

    def build_stats(self) -> ur.Text:
        aspect = ur.window.aspect_ratio
        margin = self.config.margin
        return self.make_text(
            origin=(-0.5, 0.5),
            x=-aspect / 2 + margin,
            y=0.5 - margin,
            text="",
        )

    def build_controls(self) -> None:
        aspect = ur.window.aspect_ratio
        margin = self.config.margin
        body_y = 0.5 - margin
        labels = self.make_text(
            origin=(-0.5, 0.5),
            x=0,
            y=body_y,
            text="Step\nPlay / Pause\nRestart\nRecenter\nQuit",
        )
        labels.x = aspect / 2 - margin - labels.width
        self.make_text(
            origin=(0.5, 0.5),
            x=labels.x - margin,
            y=body_y,
            text="<-/->\nSpace\nR\nC\nEsc",
        )

    def make_text(
        self,
        *,
        origin: tuple[float, float],
        x: float,
        y: float,
        text: str,
    ) -> ur.Text:
        return ur.Text(
            parent=ur.camera.ui,
            font=self.config.font,
            scale=self.config.scale,
            color=self.config.color,
            origin=origin,
            x=x,
            y=y,
            text=text,
            start_tag="§",
            end_tag="¶",
        )

    def update(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        total = len(self.animator.movements)
        current = self.animator.state.current_step
        drones_total = len(self.animator.cars)
        end_hub = self.animator.data.end_hub
        arrived = sum(
            1 for pos in self.animator.trajectory.state_at(current).values()
            if pos == end_hub
        )
        if current >= total:
            state = "Done"
        elif self.animator.state.autoplay:
            state = "Playing"
        else:
            state = "Paused"
        self.stats.text = (
            f"Total: {total} turns\n"
            f"Step: {current}/{total}\n"
            f"Drones arrived: {arrived}/{drones_total}\n"
            f"State: {state}"
        )
