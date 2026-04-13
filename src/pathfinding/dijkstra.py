from graph import GraphType


class Dijkstra:
    @staticmethod
    def run(
        graph: GraphType,
        start: str,
    ) -> tuple[dict[str, float], dict[str, str | None]]:
        nodes = set(graph.keys())
        for edges in graph.values():
            for v, _ in edges:
                nodes.add(v)

        dist: dict[str, float] = {n: float("inf") for n in nodes}
        prev: dict[str, str | None] = {n: None for n in nodes}
        visited: set[str] = set()

        dist[start] = 0

        while len(visited) < len(nodes):
            current = None
            best = float("inf")

            for n in nodes:
                if n not in visited and dist[n] < best:
                    best = dist[n]
                    current = n

            if current is None:
                break

            visited.add(current)

            for neighbor, w in graph.get(current, []):
                if neighbor in visited:
                    continue

                new = dist[current] + w

                if new < dist[neighbor]:
                    dist[neighbor] = new
                    prev[neighbor] = current

        return dist, prev


def reconstruct(
    prev: dict[str, str | None],
    start: str,
    end: str,
) -> list[str]:
    path: list[str] = []
    cur: str | None = end

    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]

    return path[::-1] if path[-1] == start else []
