from models import MapData
from typing import TypeAlias
from pathlib import Path
from parsing import Parser
from .simulator import Simulator

Simulations: TypeAlias = dict[str, list[list[str]]]


class Benchmark:
    BUCKET_ORDER = ["easy", "medium", "hard", "challenger"]

    def __init__(self) -> None:
        maps_paths: list[Path] = self.get_maps()
        maps: dict[str, MapData] = self.parse_maps(maps_paths)
        simulations: Simulations = self.simulate_maps(maps)
        self.report_benchmark(simulations)

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
    def parse_maps(maps_path: list[Path]) -> dict[str, MapData]:
        maps_data: dict[str, MapData] = {}
        for path in maps_path:
            name = f"{path.parent.name.capitalize()}: {path.name}"
            data = Parser().parse(str(path))
            maps_data[name] = data
        return maps_data

    @staticmethod
    def simulate_maps(maps: dict[str, MapData]) -> Simulations:
        simulations: Simulations = {}
        for name, map in maps.items():
            simulation = Simulator(map).simulate()
            simulations[name] = simulation
        return simulations

    @staticmethod
    def report_benchmark(simulations: Simulations) -> None:
        with open("bench.txt", "w") as f:
            for name, simulation in simulations.items():
                f.write(f"{name}: {len(simulation)} turns\n")
