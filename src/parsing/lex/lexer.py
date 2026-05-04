from pathlib import Path
from models.limits import Limits
from ..errors import MapError
from .metadata import MetadataParser
from .result import Entry, LexResult


class Lexer:
    VALID_PREFIXES: tuple[str, ...] = (
        "nb_drones",
        "start_hub",
        "end_hub",
        "hub",
        "connection",
    )

    def lex(self, path: str | Path) -> LexResult:
        text = self.read_text(path)
        nb_drones: int | None = None
        start_hub: Entry | None = None
        end_hub: Entry | None = None
        hubs: list[Entry] = []
        connections: list[Entry] = []

        for line_no, line in enumerate(text.splitlines(), start=1):
            if len(line) > Limits.max_line_len:
                raise MapError("line is too long", line_no, line)
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            prefix, value = self.split_prefix(stripped, line_no)

            if nb_drones is None and prefix != "nb_drones":
                raise MapError(
                    "first non-comment line must be 'nb_drones'",
                    line_no,
                    line,
                )

            if prefix == "nb_drones":
                if nb_drones is not None:
                    raise MapError(
                        "nb_drones declared more than once",
                        line_no,
                        line,
                    )
                nb_drones = self.parse_int(value, line_no, line)
            elif prefix == "start_hub":
                if start_hub is not None:
                    raise MapError(
                        "start_hub declared more than once",
                        line_no,
                        line,
                    )
                start_hub = (line_no, self.lex_hub(value, line_no, line))
            elif prefix == "end_hub":
                if end_hub is not None:
                    raise MapError(
                        "end_hub declared more than once",
                        line_no,
                        line,
                    )
                end_hub = (line_no, self.lex_hub(value, line_no, line))
            elif prefix == "hub":
                hubs.append((line_no, self.lex_hub(value, line_no, line)))
            else:
                connections.append(
                    (line_no, self.lex_connection(value, line_no, line))
                )

        if nb_drones is None:
            raise MapError("missing nb_drones")
        if start_hub is None:
            raise MapError("missing start_hub")
        if end_hub is None:
            raise MapError("missing end_hub")

        return LexResult(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=connections,
        )

    @staticmethod
    def read_text(path: str | Path) -> str:
        if not str(path).strip():
            raise MapError("no file path provided")
        p = Path(path)
        if not p.exists():
            raise MapError(f"file not found: {path}")
        if not p.is_file():
            raise MapError(f"not a valid file: {path}")
        size = p.stat().st_size
        if size > Limits.max_file_size:
            raise MapError("file is too heavy")
        try:
            return p.read_text(encoding="utf-8", errors="strict")
        except Exception as e:
            raise MapError(f"Error reading file: {e}") from e

    def split_prefix(self, line: str, line_no: int) -> tuple[str, str]:
        if ":" not in line:
            raise MapError("missing ':' separator", line_no, line)
        prefix, value = line.split(":", 1)
        prefix, value = prefix.strip(), value.strip()
        if prefix not in self.VALID_PREFIXES:
            raise MapError(
                f"unknown entity type '{prefix}'",
                line_no,
                line,
            )
        if not value:
            raise MapError(f"'{prefix}' has no value", line_no, line)
        return prefix, value

    @staticmethod
    def parse_int(value: str, line_no: int, line: str) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise MapError(
                f"expected an integer, got '{value}'",
                line_no,
                line,
            ) from e

    @staticmethod
    def lex_hub(value: str, line_no: int, line: str) -> dict[str, str]:
        head, meta = MetadataParser.split_brackets(value, line_no, line)
        parts = head.split()
        if len(parts) != 3:
            raise MapError(
                "hub expects 'name x y [metadata]'",
                line_no,
                line,
            )

        name, x, y = parts
        if "-" in name:
            raise MapError(
                f"hub name cannot contain '-': '{name}'",
                line_no,
                line,
            )
        fields = MetadataParser.parse(
            meta,
            Limits.allowed_hub_keys,
            line_no,
            line,
        )
        fields.update({"name": name, "x": x, "y": y})
        return fields

    @staticmethod
    def lex_connection(
        value: str,
        line_no: int,
        line: str,
    ) -> dict[str, str]:
        head, meta = MetadataParser.split_brackets(value, line_no, line)
        if head.count("-") != 1:
            raise MapError(
                "connection expects 'name1-name2'",
                line_no,
                line,
            )

        a, b = head.split("-")
        a, b = a.strip(), b.strip()
        if not a or not b:
            raise MapError("connection has empty hub name", line_no, line)
        fields = MetadataParser.parse(
            meta,
            Limits.allowed_connection_keys,
            line_no,
            line,
        )
        fields.update({"a": a, "b": b})
        return fields
