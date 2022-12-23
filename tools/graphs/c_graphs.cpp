#include "c_graphs.h"
#include <algorithm>
#include <queue>

void Graph::set_graph(graph_t graph, node_index_t start_node)
{
  this->graph = graph;
  this->start_node = start_node;
  this->reset();
}

Graph::Graph(graph_t graph, node_index_t start_node)
{
  set_graph(graph, start_node);
}

Graph::Graph(adjency_matrix_t adj_matrix, node_index_t start_node)
{
  const size_t num_nodes = adj_matrix.size();
  graph_t graph;
  graph.resize(num_nodes);
  for (node_index_t i = 0; i < num_nodes; i++)
  {
    graph[i].index = i;
    for (node_index_t j = 0; j < num_nodes; j++)
    {
      if (adj_matrix[i][j] != 0)
      {
        graph[i].links.push_back({adj_matrix[i][j], &graph[j]});
      }
    }
  }
  set_graph(graph, start_node);
}

void Graph::reset(void)
{
    // Clear the queue and visited set
    queue.clear();

    // Add the start node to the queue as a single-node path
    path_t start_path = { start_node };
    queue.push_back(start_path);
}

path_t Graph::get_next_path_bft()
{
    // If the queue is empty, return an empty path
    if (queue.empty())
    {
        return path_t();
    }

    // Get the next path from the queue
    path_t next_path = queue.front();
    visited_t visited = visited_t(next_path.begin(),next_path.end());
    queue.pop_front();

    // Get the last node in the path
    node_index_t last_node_index = next_path.back();
    node_t& last_node = graph[last_node_index];

    // Iterate through the links of the last node
    for (const auto& link : last_node.links)
    {
        // If the linked node has not been visited
        if (visited.find(link.node->index) == visited.end())
        {
            // Mark the linked node as visited
            visited.insert(link.node->index);

            // Create a new path by appending the linked node to the current path
            path_t new_path = next_path;
            new_path.push_back(link.node->index);

            // Add the new path to the queue
            queue.push_back(new_path);
        }
    }

    return next_path;
}


std::vector<std::vector<size_t>> Graph::floyd_warshall()
{
    // Initialize the distance matrix with the weights of the links
    size_t num_nodes = graph.size();
    std::vector<std::vector<size_t>> distance(num_nodes, std::vector<size_t>(num_nodes, std::numeric_limits<size_t>::max()));
    for (size_t i = 0; i < num_nodes; i++)
    {
        distance[i][i] = 0;
        for (const link_t& link : graph[i].links)
        {
            distance[i][link.node->index] = link.weight;
        }
    }

    // Perform the Floyd-Warshall algorithm
    for (size_t k = 0; k < num_nodes; k++)
    {
        for (size_t i = 0; i < num_nodes; i++)
        {
            for (size_t j = 0; j < num_nodes; j++)
            {
                distance[i][j] = std::min(distance[i][j], distance[i][k] + distance[k][j]);
            }
        }
    }

    return distance;
}
