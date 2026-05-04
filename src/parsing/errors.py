class MapError(Exception):
    def __init__(
        self,
        message: str,
        line_no: int | None = None,
        line: str | None = None,
    ) -> None:
        self.message: str = message
        self.line_no: int | None = line_no
        self.line: str | None = line
        super().__init__(self.format())

    def format(self) -> str:
        if self.line_no is None:
            return self.message
        return f"line {self.line_no}: {self.message}"
