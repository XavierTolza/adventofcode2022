#include <vector>
#include <stdint.h>
#include <set>
#include <deque>

#define WEIGHT_IS_LINK(w) (w > 0)

typedef size_t node_index_t;
typedef uint32_t weight_t;
typedef std::vector<node_index_t> path_t;
typedef std::deque<path_t> queue_t;
typedef std::set<node_index_t> visited_t;
typedef std::vector<std::vector<weight_t>> adjency_matrix_t;

class Graph
{
private:
    adjency_matrix_t graph;
    queue_t queue;
    node_index_t start_node;


public:
    Graph(adjency_matrix_t graph, node_index_t start_node);
    void reset(void);

    path_t get_next_path_bft();
    std::vector<std::vector<weight_t>> floyd_warshall();
};