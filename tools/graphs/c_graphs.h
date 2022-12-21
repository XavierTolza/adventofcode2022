#include <vector>
#include <stdint.h>
#include <set>

typedef size_t node_t;
typedef std::vector<node_t> path_t;
typedef std::vector<path_t> queue_t;
typedef std::set<node_t> visited_t;
typedef std::vector<std::vector<node_t>> graph_t;

typedef enum _traversal_t{
    BREADTH,
    DEPTH
} traversal_t;

path_t c_get_next_path(graph_t &graph, traversal_t traversal_mode, queue_t &queue, visited_t &visited);