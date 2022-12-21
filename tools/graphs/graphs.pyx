from graphs cimport c_get_next_path

def get_next_path(graph, traversal_mode, queue=None, visited=None):
    cdef graph_t c_graph = graph
    cdef queue_t c_queue
    cdef visited_t c_visited
    if queue is not None:
        c_queue = queue
    if visited is not None:
        c_visited = visited
    return get_next_path(c_graph, traversal_mode, c_queue, c_visited)