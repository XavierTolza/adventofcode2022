from typing import Callable, List

from graphviz import Digraph


def all_paths(graph: List[List[int]], breadth_first: bool = True) -> List[List[int]]:
    """Generate all possible paths in a graph using a breadth-first or depth-first search.

    Parameters:
    graph (List[List[int]]): The adjacency matrix representation of the graph.
    breadth_first (bool, optional): Whether to perform a breadth-first or depth-first search. Defaults to True.

    Returns:
    List[List[int]]: A list of lists representing the paths in the graph.
    """
    # Initialize the queue or stack for the search
    queue = [[0]] if breadth_first else [[0]][::-1]
    # Initialize a set to store the visited nodes
    visited = set()
    # Initialize a list to store the paths
    paths = []

    # Perform the search
    while queue:
        # Get the next path from the queue or stack
        path = queue.pop(0) if breadth_first else queue.pop()
        # Get the last node in the path
        node = path[-1]
        # If the node has not been visited yet
        if node not in visited:
            # Mark the node as visited
            visited.add(node)
            # Add the path to the list of paths
            paths.append(path)
            # Add all the neighbors of the node to the queue or stack
            for i, weight in enumerate(graph[node]):
                if weight != 0:
                    new_path = path.copy()
                    new_path.append(i)
                    queue.append(new_path) if breadth_first else queue.insert(
                        0, new_path
                    )

    return paths


def minimum_cost_path(
    graph: List[List[int]],
    max_length: int,
    path_length: Callable[List[int], float],
    path_cost: Callable[List[int], float],
    **kwargs
) -> List[int]:
    # Initialize the minimum cost path to be empty
    min_cost_path = []
    # Initialize the minimum cost to be infinity
    min_cost = float("inf")

    # Iterate over all possible paths in the graph
    for path in all_paths(graph, **kwargs):
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
