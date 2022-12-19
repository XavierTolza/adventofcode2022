from typing import Callable, List

from graphviz import Digraph


def dfs_paths(graph, start: int = 0, path=[]):
    """
    Find all paths in a graph using depth-first search.

    Parameters
    ----------
    graph : numpy.ndarray
        A square matrix representing the graph, where each element graph[i, j] represents the weight
        of the edge between the vertices i and j. The vertices are represented by integers, starting
        from 0.
    start : int
        The starting vertex for the search.
    path : list, optional
        The current path being explored, by default an empty list.

    Returns
    -------
    list of list of int
        A list of lists, where each inner list represents a path in the graph.

    """

    # add the current vertex to the path
    path = path + [start]

    # initialize the list of paths
    paths = []

    # explore all the vertices that can be reached from the current vertex
    for vertex in range(graph.shape[0]):
        # if there is an edge between the current vertex and the vertex being explored
        if graph[start, vertex] != 0:
            # if the vertex has not been visited yet
            if vertex not in path:
                # find the paths starting from the vertex being explored
                extended_paths = dfs_paths(graph, vertex, path)
                # add the extended paths to the list of paths
                for p in extended_paths:
                    paths.append(p)
                paths.append(path)

    # return the list of paths
    return paths


def bfs_paths(graph, start):
    """
    Find all paths in a graph using breadth-first search.

    Parameters
    ----------
    graph : numpy.ndarray
        A square matrix representing the graph, where each element graph[i, j] represents the weight
        of the edge between the vertices i and j. The vertices are represented by integers, starting
        from 0.
    start : int
        The starting vertex for the search.

    Returns
    -------
    list of list of int
        A list of lists, where each inner list represents a path in the graph.

    """

    # initialize the queue with the starting vertex
    queue = [[start]]

    # initialize the list of paths
    paths = []

    # while the queue is not empty
    while queue:
        # get the first path in the queue
        path = queue.pop(0)
        # get the last vertex in the path
        vertex = path[-1]
        # explore all the vertices that can be reached from the current vertex
        for next_vertex in range(graph.shape[0]):
            # if there is an edge between the current vertex and the vertex being explored
            if graph[vertex, next_vertex] != 0:
                # create a new path by extending the current path with the vertex being explored
                new_path = path + [next_vertex]
                # if the vertex has not been visited yet
                if next_vertex not in path:
                    # add the new path to the list of paths
                    paths.append(new_path)
                    # add the new path to the queue
                    queue.append(new_path)

    # return the list of paths
    return paths


def minimum_cost_path(
    graph: List[List[int]],
    max_length: int,
    path_length: Callable[[List[int]], float],
    path_cost: Callable[[List[int]], float],
    **kwargs
) -> List[int]:
    # Initialize the minimum cost path to be empty
    min_cost_path = []
    # Initialize the minimum cost to be infinity
    min_cost = float("inf")

    # Iterate over all possible paths in the graph
    for path in dfs_paths(graph, **kwargs):
        # Calculate the length of the path
        length = path_length(path)
        # If the length of the path exceeds the maximum length, skip it
        if length > max_length:
            continue
        # Calculate the cost of the path
        cost = path_cost(path)
        # If the cost of the path is less than the current minimum cost, update the minimum cost and the minimum cost path
        if cost < min_cost:
            min_cost = cost
            min_cost_path = path

    return min_cost_path


def floyd_warshall(graph: List[List[int]]):
    """Implement the Floyd-Warshall algorithm to compute the shortest paths between all pairs of nodes in a graph.

    Parameters:
    graph (List[List[int]]): The adjacency matrix representation of the graph.

    Returns:
    A 2D array representing the shortest path distances between all pairs of nodes.
    """
    n = len(graph)

    # Initialise la distance entre chaque paire de sommets à l'infini
    distance = [[float("inf") for _ in range(n)] for _ in range(n)]

    # Initialise la distance entre chaque sommet à 0
    for i in range(n):
        distance[i][i] = 0

    # Remplit la matrice de distance en utilisant les valeurs de l'adjacence
    for i in range(n):
        for j in range(n):
            if graph[i][j] != float("inf"):
                distance[i][j] = graph[i][j]

    # Applique l'algorithme de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    return distance


def generate_graph_svg(
    graph: List[List[int]], labels: List[str], file_path: str
) -> None:
    """Generate an SVG visual representation of a graph using Graphviz and save it to a file.

    Parameters:
    graph (List[List[int]]): The adjacency matrix representation of the graph.
    labels (List[str]): A list of labels for each node in the graph.
    file_path (str): The path to the file where the graph will be saved.

    Returns:
    None
    """
    dot = Digraph()

    # Add nodes to the graph
    for i, label in enumerate(labels):
        dot.node(str(i), label)

    # Add edges to the graph
    for i, row in enumerate(graph):
        for j, weight in enumerate(row):
            if weight != 0:
                dot.edge(str(i), str(j), str(weight))

    # Generate the SVG file
    dot.render(file_path, format="svg")
