import pytest
import numpy as np
from tools.graphs import PyGraph



@pytest.fixture
def adj_matrix():
    # Create an adjacency matrix for a graph with 4 nodes and 6 links
    res = [[0, 1, 2, 0], 
           [0, 0, 0, 3], 
           [0, 0, 0, 4], 
           [0, 0, 0, 0]]
    return np.array(res)


@pytest.fixture
def g(adj_matrix):
    return PyGraph(adj_matrix, 0)


def test_get_next_path_bft(g):
    # Expected paths in the breadth-first traversal
    expected_paths = [[0], [0, 1], [0, 2], [0, 1, 3], [0, 2, 3]]

    # Iterate through the expected paths and compare them to the paths returned by get_next_path_bft
    for path, expected_path in zip(g.iter_paths_bft(), expected_paths):
        assert path == expected_path


def test_get_path_by_length(g):
    res = list(g.iter_paths_by_length(as_numpy_array=False))
    expected_paths = [[[0]], [[0, 1], [0, 2]], [[0, 1, 3], [0, 2, 3]]]
    assert res==expected_paths
    
def test_floyd_warshall(g,adj_matrix):
    with pytest.raises(ValueError):
        distance = g.floyd_warshall()
    
    m2 = adj_matrix+adj_matrix.T
    print(m2)
    g2 = PyGraph(m2,0)
    distance = g2.floyd_warshall()
    raise NotImplementedError