from dataclasses import dataclass
from pathlib import Path
from parsing import Parser
from .simulator import Simulator


@dataclass(frozen=True)
class BenchEntry:
    name: str
    turns: int | None = None
    error: str | None = None


class Benchmark:
    BUCKET_ORDER = ["easy", "medium", "hard", "challenger"]

    def __init__(self) -> None:
        paths = self.get_maps()
        entries = [self.run_map(p) for p in paths]
        self.report(entries)

    @staticmethod
    def get_maps() -> list[Path]:
        folder = Path("assets")
        paths = list(folder.rglob("*.txt"))

        def sort_key(p: Path) -> tuple[int, str, str]:
            bucket = p.parent.name
            rank = (
                Benchmark.BUCKET_ORDER.index(bucket)
                if bucket in Benchmark.BUCKET_ORDER
                else len(Benchmark.BUCKET_ORDER)
            )
            return (rank, bucket, p.name)

        return sorted(paths, key=sort_key)

    @staticmethod
    def run_map(path: Path) -> BenchEntry:
        name = f"{path.parent.name.capitalize()}: {path.name}"
        try:
            data = Parser().parse(str(path))
            simulation = Simulator(data).simulate()
        except Exception as e:
            return BenchEntry(name=name, error=str(e))
        return BenchEntry(name=name, turns=len(simulation))

    @staticmethod
    def report(entries: list[BenchEntry]) -> None:
        with open("bench.txt", "w") as f:
            for entry in entries:
                if entry.error is not None:
                    f.write(f"{entry.name}: ERROR -> {entry.error}\n")
                else:
                    f.write(f"{entry.name}: {entry.turns} turns\n")
