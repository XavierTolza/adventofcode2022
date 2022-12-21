#include "c_graphs.h"

path_t c_get_next_path(graph_t &graph, traversal_t traversal_mode, queue_t &queue, visited_t &visited) {
  if (queue.empty()) {
    return {};
  }

  path_t curr_path = queue.front();
  queue.erase(queue.begin());
  node_t curr_node = curr_path.back();

  if (visited.find(curr_node) != visited.end()) {
    return c_get_next_path(graph, traversal_mode, queue, visited);
  }
  visited.insert(curr_node);

  for (node_t next_node : graph[curr_node]) {
    path_t next_path = curr_path;
    next_path.push_back(next_node);
    if (traversal_mode == BREADTH) {
      queue.push_back(next_path);
    } else {
      queue.insert(queue.begin(), next_path);
    }
  }

  return curr_path;
}