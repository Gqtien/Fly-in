import ursina as ur
from ..animation import Animator
from .camera import Camera


class Controller(ur.Entity):
    def __init__(self, camera: Camera, animator: Animator) -> None:
        super().__init__()
        self.camera: Camera = camera
        self.animator: Animator = animator

    def input(self, key: str) -> None:
        match key:
            case "escape":
                ur.application.quit()
            case "c":
                self.camera.reset()
            case "space":
                self.animator.toggle_autoplay()
            case "right arrow":
                self.animator.step_forward()
            case "left arrow":
                self.animator.step_backward()
            case "r":
                self.animator.restart()
