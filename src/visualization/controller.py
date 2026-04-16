import ursina as ur
from models import MapData
from .computer import Computer


class Controller(ur.Entity):
    def __init__(self, data: MapData) -> None:
        super().__init__()
        self.data = data
        self.computer = Computer(self.data)
        self.cam_pos = self.computer.compute_camera_pos()

    def update(self) -> None:
        ...

    def input(self, key: str) -> None:
        match key:
            case "escape":
                ur.application.quit()
            case "r":
                self.recenter()

    def recenter(self) -> None:
        ur.camera.position = (*self.cam_pos,)
