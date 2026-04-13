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
        self.drones: int = 0

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
