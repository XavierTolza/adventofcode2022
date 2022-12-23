# distutils: language = c++
# distutils: sources = tools/graphs/c_graphs.cpp
# distutils: include_dirs = tools/graphs

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
        void reset() nogil
        path_t get_next_path_bft() nogil
        path_t get_next_path_dft() nogil
        vector[vector[size_t]] floyd_warshall();
        

# Define a Python wrapper class for the C++ Graph class
cdef class PyGraph:
    cdef Graph *c_graph
    cdef char is_directive

    def __cinit__(self, adj_matrix: np.ndarray, start_node: int=0):
        self.c_graph = new Graph(<adjency_matrix_t>adj_matrix, <node_index_t>start_node)
        self.is_directive = not np.all(np.transpose(adj_matrix)==adj_matrix)
    
    def iter_paths_bft(self) -> list:
        self.c_graph.reset()
        while True:
            path = self.c_graph.get_next_path_bft()
            if len(path)==0:
                self.c_graph.reset()
                break
            yield path

    def iter_paths_by_length(self, as_numpy_array:bool=False)->list:
        cdef vector[path_t] res
        with nogil:
            while True:
                path = self.c_graph.get_next_path_bft()
                if path.size()==0:
                    with gil:
                        if as_numpy_array:
                            yield np.array(res)
                        else:
                            yield res
                    break
                if res.size()>0 and path.size()!=res.back().size():
                    with gil:
                        if as_numpy_array:
                            yield np.array(res)
                        else:
                            yield res
                    res.clear()
                res.push_back(path)

    def floyd_warshall(self)->np.ndarray:
        if self.is_directive:
            raise ValueError("floyd_warshall does not support directive graphs")
        return np.array(self.c_graph.floyd_warshall())

    min_distance_between_two_nodes = floyd_warshall