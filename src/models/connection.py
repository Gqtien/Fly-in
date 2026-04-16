from .drone import Drone


class Connection:
    def __init__(
        self,
        from_hub: str,
        to_hub: str,
        max_link_capacity: int | None = None,
    ):
        self.from_hub: str = from_hub
        self.to_hub: str = to_hub
        self.max_link_capacity: int | None = max_link_capacity
        self.drones: list[Drone] = []

    def has_capacity(self) -> bool:
        return (
            self.max_link_capacity is None
            or len(self.drones) < self.max_link_capacity
        )

    def add_drone(self, drone: Drone) -> bool:
        if (
            self.max_link_capacity is None
            or len(self.drones) + 1 <= self.max_link_capacity
        ) and drone not in self.drones:
            self.drones.append(drone)
            return True
        return False

    def remove_drone(self, drone: Drone) -> bool:
        if drone in self.drones:
            self.drones.remove(drone)
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.from_hub} -> {self.to_hub} "
            f"(drones: {len(self.drones)}/{self.max_link_capacity})"
        )
