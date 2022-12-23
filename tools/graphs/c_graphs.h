#include <vector>
#include <stdint.h>
#include <set>

typedef size_t node_index_t;
typedef uint32_t weight_t;
struct _node_t;
typedef struct _link_t
{
    weight_t weight;
    struct _node_t *node;
} link_t;
typedef struct _node_t
{
    node_index_t index;
    weight_t weight;
    std::vector<link_t> links;
} node_t;
typedef std::vector<node_index_t> path_t;
typedef std::vector<path_t> queue_t;
typedef std::set<node_index_t> visited_t;
typedef std::vector<node_t> graph_t;
typedef std::vector<std::vector<weight_t>> adjency_matrix_t;

typedef enum _traversal_t
{
    BREADTH,
    DEPTH
} traversal_t;

class Graph
{
private:
    graph_t graph;
    queue_t queue;
    visited_t visited;
    node_index_t start_node;

    void set_graph(graph_t graph, node_index_t start_node);

public:
    Graph(graph_t graph, node_index_t start_node);
    Graph(adjency_matrix_t adj_matrix, node_index_t start_node);
    void reset(void);

    path_t get_next_path_bft();
    path_t get_next_path_dft();
};