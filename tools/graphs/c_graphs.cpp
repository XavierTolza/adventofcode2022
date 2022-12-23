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
  for (node_index_t i = 0; i < num_nodes; ++i)
  {
    graph[i].index = i;
    for (node_index_t j = 0; j < num_nodes; ++j)
    {
      if (adj_matrix[i][j] != 0)
      {
        graph[i].links.push_back({adj_matrix[i][j], &graph[j]});
      }
    }
  }
  set_graph(graph, start_node);
}

void Graph::reset()
{
  queue.clear();
  visited.clear();
  queue.push_back({this->start_node});
}

path_t Graph::get_next_path_bft()
{
  node_t node;
  node_index_t node_index;
  path_t res;
  path_t path;

  // Find the next nodes
  std::vector<link_t>::iterator it;
  link_t link;
  do
  {
    path = queue.front();
    node_index = path.back();
    node = graph.at(node_index);

    for (it = node.links.begin(); it != node.links.end(); it++)
    {
      link = *it;
      if (visited.count(link.node->index) == 0)
      {
        // We found next node to seek
        res = path_t(path);
        res.push_back(node_index);
        visited.insert(node_index);
        return res;
      }
      queue.pop_front();
    }
  } while (!queue.empty());
  return {};
}

path_t Graph::get_next_path_dft()
{
  reset();
  std::vector<node_index_t> stack;
  stack.push_back(start_node);
  while (!stack.empty())
  {
    node_index_t node_index = stack.back();
    stack.pop_back();
    node_t node = graph[node_index];
    if (visited.count(node.index) > 0)
      continue;
    visited.insert(node.index);
    for (const link_t &link : node.links)
    {
      if (visited.count(link.node->index) > 0)
        continue;
      stack.push_back(link.node->index);
    }
  }
  return {}; // Return an empty path if no more paths are found
}
