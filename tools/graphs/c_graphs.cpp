#include "c_graphs.h"
#include <algorithm>
#include <queue>

Graph::Graph(adjency_matrix_t graph, node_index_t start_node)
{
  this->graph = graph;
  this->start_node = start_node;
  this->reset();
}

void Graph::reset(void)
{
  // Clear the queue and visited set
  queue.clear();

  // Add the start node to the queue as a single-node path
  path_t start_path = {start_node};
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
  visited_t visited = visited_t(next_path.begin(), next_path.end());
  queue.pop_front();

  // Get the last node in the path
  node_index_t last_node_index = next_path.back();

  // Iterate through the links of the last node
  node_index_t link_index;
  bool link_visited;

  for (link_index = 0; link_index < graph.size(); link_index++)
  {
    weight_t link = graph[last_node_index][link_index];
    link_visited = visited.find(link_index) != visited.end();

    // If the linked node has not been visited
    if ((!link_visited) && WEIGHT_IS_LINK(link))
    {
      // Mark the linked node as visited
      visited.insert(link_index);

      // Create a new path by appending the linked node to the current path
      path_t new_path = next_path;
      new_path.push_back(link_index);

      // Add the new path to the queue
      queue.push_back(new_path);
    }
  }

  return next_path;
}

std::vector<std::vector<weight_t>> Graph::floyd_warshall() {
  size_t n = graph.size();
  weight_t limit = std::numeric_limits<weight_t>::max();
  std::vector<std::vector<weight_t>> dist(n, std::vector<weight_t>(n, limit));

  // Initialize distances between each pair of vertices
  for (size_t i = 0; i < n; ++i) {
    for (size_t j = 0; j < n; ++j) {
      if (WEIGHT_IS_LINK(graph[i][j])) {
        dist[i][j] = graph[i][j];
      }
      if (i==j){
        dist[i][j]=0;
      }
    }
  }

  // Apply Floyd-Warshall algorithm
  for (size_t k = 0; k < n; ++k) {
    for (size_t i = 0; i < n; ++i) {
      for (size_t j = 0; j < n; ++j) {
        if ((dist[i][k] != limit && dist[k][j] != limit && dist[i][j] > dist[i][k] + dist[k][j]) && (i!=j)) {
          dist[i][j] = dist[i][k] + dist[k][j];
        }
      }
    }
  }

  return dist;
}
