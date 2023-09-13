import re
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple

import networkx as nx
from matplotlib import pyplot as plt


def get_pattern() -> Tuple[re.Pattern[str], Tuple[str, ...]]:
    pattern = r'e (?P<vertices_1>\d+) (?P<vertices_2>\d+)'
    pattern_group = ('vertices_1', 'vertices_2')

    compiled_pattern = re.compile(pattern)
    return compiled_pattern, pattern_group


class Graph:
    def __init__(self) -> None:
        self._data = defaultdict(list)
  
    def read(self, file: Path):
        edge_pattern, edge_group = get_pattern()

        with file.open() as f:
            for data_string in f.readlines():
                if match := edge_pattern.match(data_string):
                    vertex_1 = int(match.group(edge_group[0]))
                    vertex_2 = int(match.group(edge_group[1]))

                    if vertex_2 not in self._data[vertex_1]:
                        self._data[vertex_1].append(vertex_2)
                    if vertex_1 not in self._data[vertex_2]:
                        self._data[vertex_2].append(vertex_1)
    
    def neighbors(self, vertex: int) -> list[int]:
        return self._data[vertex]

    @property
    def vertexes(self) -> list[int]:
        return [int(vertex) for vertex in self._data]
    
    @property
    def num_vertex(self) -> int:
        return len(self.vertexes)

    def as_dict(self) -> dict[int, int]:
        return dict(self._data)
    
    def as_graph(self) -> nx.Graph:
        return nx.from_dict_of_lists(self.as_dict())
    
    def save_as_graph(self, path: Path = Path('graph.png'), figsize: Optional[Tuple[int, int]] = None) -> None:
        nx_graph = self.as_graph()
        pos = nx.spring_layout(nx_graph, seed=225)
        fig = plt.figure(figsize=figsize, layout='tight')
        nx.draw(nx_graph, pos, ax=fig.add_subplot())
        fig.savefig(path)


if __name__ == '__main__':
    graph = Graph()
    graph.read(Path('tests/example.col'))

    graph.save_as_graph()