from libcpp.vector cimport vector
from libcpp.set cimport set

cdef extern from "c_graphs.h":
    ctypedef size_t node_t
    ctypedef vector[node_t] path_t
    ctypedef vector[path_t] queue_t
    ctypedef set[node_t] visited_t
    ctypedef vector[vector[node_t]] graph_t
    cdef enum _traversal_t:
        BREADTH
        DEPTH

    path_t c_get_next_path(graph_t &graph, _traversal_t traversal_mode, queue_t &queue, visited_t &visited)
