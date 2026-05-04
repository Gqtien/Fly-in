from ..errors import MapError


class MetadataParser:
    @staticmethod
    def split_brackets(
        value: str,
        line_no: int,
        line: str,
    ) -> tuple[str, str]:
        opens = value.count("[")
        closes = value.count("]")

        if opens == 0 and closes == 0:
            return value.strip(), ""

        if opens != 1 or closes != 1:
            raise MapError("malformed metadata brackets", line_no, line)

        if not value.endswith("]"):
            raise MapError("metadata bracket not closed", line_no, line)

        bracket_start = value.index("[")
        head = value[:bracket_start].strip()
        meta = value[bracket_start + 1:-1]
        return head, meta

    @staticmethod
    def parse(
        meta: str,
        allowed: frozenset[str],
        line_no: int,
        line: str,
    ) -> dict[str, str]:
        if not meta.strip():
            return {}

        result: dict[str, str] = {}
        for entry in meta.split():
            if "=" not in entry:
                raise MapError(
                    f"metadata entry '{entry}' missing '='",
                    line_no,
                    line,
                )

            key, _, val = entry.partition("=")
            if key not in allowed:
                raise MapError(
                    f"unknown metadata key '{key}'",
                    line_no,
                    line,
                )

            if key in result:
                raise MapError(
                    f"duplicate metadata key '{key}'",
                    line_no,
                    line,
                )

            if not val:
                raise MapError(
                    f"metadata key '{key}' has empty value",
                    line_no,
                    line,
                )

            result[key] = val
        return result
