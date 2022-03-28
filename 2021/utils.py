import cmath
import networkx as nx
import numpy as np
import re

def rotate_complex(complex_num, radians):
    return complex_num * cmath.exp(1j * radians)

def extract_ints(raw: str):
    return list(map(int, re.findall(r"(\d+)", raw)))

def extract_int_lines(lines: list[str]):
    return [list(map(int, re.findall(r"(\d+)", line))) for line in lines]

def extract_maze(raw: str, empty_cell=".", largest_component=False):
    """
    Parse an ascii maze into a networkx graph. Return a tuple `(np.array, nx.Graph)`.
    """

    maze = np.array(
        [[*line] for line in raw.splitlines()]
    )

    G = nx.grid_graph(maze.shape[::-1])

    walls = np.stack(np.where(maze != empty_cell)).T
    G.remove_nodes_from(map(tuple, walls))

    if largest_component:
        G.remove_nodes_from(G.nodes - max(nx.connected_components(G), key=lambda g: len(g)))

    return maze, G
