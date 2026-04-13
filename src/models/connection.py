class Connection:
    def __init__(
        self,
        from_hub: str,
        to_hub: str,
        max_link_capacity: int | None = None,
    ):
        self.from_hub = from_hub
        self.to_hub = to_hub
        self.max_link_capacity = max_link_capacity
        self.drones = 0

    def add_drone(self) -> bool:
        if (
            self.max_link_capacity is None
            or self.drones < self.max_link_capacity
        ):
            self.drones += 1
            return True
        return False

    def remove_drone(self) -> bool:
        if self.drones > 0:
            self.drones -= 1
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.from_hub} -> {self.to_hub} "
            f"(drones: {self.drones}/{self.max_link_capacity})"
        )
