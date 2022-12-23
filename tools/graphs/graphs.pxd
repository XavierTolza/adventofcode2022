from libcpp.vector cimport vector
from libcpp.set cimport set
from libc.stdint cimport *


cdef extern from "c_graphs.h":
    ctypedef size_t node_index_t
    ctypedef uint32_t weight_t
    ctypedef struct _node_t:
        node_index_t index
        weight_t weight
        vector[link_t] links
    ctypedef struct _link_t:
        weight_t weight
        _node_t *node
    ctypedef vector[node_index_t] path_t
    ctypedef vector[path_t] queue_t
    ctypedef set[node_index_t] visited_t
    ctypedef vector[node_t] graph_t
    ctypedef vector[vector[weight_t]] adjency_matrix_t
    ctypedef enum _traversal_t:
        BREADTH
        DEPTH

    cdef cppclass Graph:
        Graph(graph_t graph, node_index_t start_node)
        Graph(adjency_matrix_t adj_matrix, node_index_t start_node)
        void reset()
        path_t get_next_path_bft()
        path_t get_next_path_dft()