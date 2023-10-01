import random
from functools import partial
from multiprocessing import Pool, cpu_count

import networkx as nx
import numpy as np

from graph_lib.graph import Graph


def nx_clique(graph: Graph) -> list[int]:
    nx_graph = graph.as_nxgraph()
    return next(nx.find_cliques(nx_graph))


# def greedy_randomized_clique(graph: Graph, iterations: int = 10) -> list[int]:
#     best_clique = []
#     vertices = graph.vertexes

#     for _ in range(iterations):
#         clique = []
#         random_vertex = random.choice(vertices)

#         clique.append(random_vertex)

#         vertices_candidates = graph.neighbors(random_vertex)
#         np.random.shuffle(vertices_candidates)

#         for vertex in vertices_candidates:
#             is_connected = True
#             for clique_vertex in clique:
#                 if clique_vertex not in graph.neighbors(vertex):
#                     is_connected = False
#                     break
#             if is_connected:
#                 clique.append(vertex)
#         if len(clique) > len(best_clique):
#             best_clique = clique
#     return best_clique


def _get_clique(start_vertex: int, graph: Graph) -> list[int]:
    clique = [start_vertex]
    vertices_candidates = graph.neighbors(start_vertex)
    np.random.shuffle(vertices_candidates)

    for vertex in vertices_candidates:
        is_connected = True
        for clique_vertex in clique:
            if clique_vertex not in graph.neighbors(vertex):
                is_connected = False
                break
        if is_connected:
            clique.append(vertex)
    return clique


def greedy_randomized_clique(graph: Graph, iterations: int = 10, num_proc=1) -> list[int]:
    best_clique = []
    vertices = graph.vertexes

    random_vertices = np.random.choice(vertices, iterations)
    num_process = num_proc if num_proc > 1 else cpu_count()

    partial_get_clique =  partial(_get_clique, graph=graph)
    with Pool(num_process) as pool:
        cliques = pool.map(partial_get_clique, random_vertices)
    best_clique = max(cliques, key=len)
    return best_clique
