# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.set cimport set
from libc.stdint cimport *
import numpy as np

cdef extern from "c_graphs.h":
    ctypedef size_t node_index_t
    ctypedef uint32_t weight_t

    ctypedef struct _node_t:
        node_index_t index
        weight_t weight
        vector[_link_t] links

    ctypedef struct _link_t:
        weight_t weight
        _node_t* node

    ctypedef vector[node_index_t] path_t
    ctypedef vector[path_t] queue_t
    ctypedef set[node_index_t] visited_t
    ctypedef vector[_node_t] graph_t
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

# Define a Python wrapper class for the C++ Graph class
cdef class PyGraph:
    cdef Graph *c_graph

    def __cinit__(self, adj_matrix: np.ndarray, start_node: int=0):
        self.c_graph = new Graph(<adjency_matrix_t>adj_matrix, <node_index_t>start_node)

    def reset(self):
        self.c_graph.reset()

    def get_next_path_bft(self) -> list:
        return self.c_graph.get_next_path_bft()

    def get_next_path_dft(self) -> list:
        return self.c_graph.get_next_path_dft()