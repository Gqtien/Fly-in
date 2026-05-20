import ursina as ur
from panda3d.core import DepthWriteAttrib
from models import Hub
from models.zone import ZoneType
from ..config import TagConfig
from ..utils import Utils


class HubTag(ur.Entity):
    def __init__(self, hub: Hub, config: TagConfig) -> None:
        super().__init__(parent=ur.scene)
        self.config: TagConfig = config
        x, _, z = Utils.hub_world_pos(hub)
        self.position = (x, config.height_offset, z)

        if hub.type is ZoneType.BLOCKED:
            text = "X"
        elif hub.is_endpoint:
            text = config.unlimited_text
        else:
            text = str(hub.max_drones)

        sx, sy = config.shadow_offset
        self.shadow_label: ur.Text = ur.Text(
            parent=self,
            text=text,
            font=config.font,
            origin=(0, 0),
            scale=config.text_scale,
            color=config.shadow_color,
            position=(sx, -sy, 0.01),
        )
        self.shadow_label.setAttrib(
            DepthWriteAttrib.make(DepthWriteAttrib.M_off)
        )
        self.shadow_label.setBin("fixed", 19)

        self.label: ur.Text = ur.Text(
            parent=self,
            text=text,
            font=config.font,
            origin=(0, 0),
            scale=config.text_scale,
            color=(
                config.text_color
                if hub.color is not ur.color.white
                else config.accent_text_color
            ),
        )
        self.label.setBin("fixed", 20)
        self.rotation_x = 90
        self.rotation_z = 90

    def update(self) -> None:
        d = ur.camera.world_position.length()
        self.y = self.config.height_offset + max(0, d * d / 4e6)


class Tag(ur.Entity):
    def __init__(self, hubs: dict[str, Hub]) -> None:
        super().__init__()
        config = TagConfig()
        self.hub_tags: list[HubTag] = [
            HubTag(hub, config) for hub in hubs.values()
        ]
