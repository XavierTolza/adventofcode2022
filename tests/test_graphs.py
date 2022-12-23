import pytest

from tools.graphs import PyGraph


@pytest.fixture
def adjmat():
    return [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 1, 0, 1, 0],
    ]


@pytest.fixture
def graph(adjmat):
    return PyGraph(adjmat, 0)


def test_graph_creation(adjmat):
    PyGraph(adjmat, 0)


def test_bft_traversal(graph):
    path = graph.get_next_path_bft()
    path = graph.get_next_path_bft()
    path = graph.get_next_path_bft()
    path = graph.get_next_path_bft()
    path = graph.get_next_path_bft()
    raise NotImplementedError
