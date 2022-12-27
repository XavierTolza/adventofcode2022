import re

import numpy as np

from tools.graphs import PyGraph

demo_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

demo_result = 1651

matcher = re.compile(
    "Valve ([A-Z]{2}) has flow rate=(-?\d+); tunnels? leads? to valves? ([A-Z, ]+)"
)


def parse(data_str):
    data = [[i[0], (i[1], i[2].split(", "))] for i in matcher.findall(data_str)]
    data = dict(data)
    labels = np.array(list(data.keys()))
    flows = np.array([int(i[0]) for i in data.values()])
    name2index = {k: i for k, i in zip(data.keys(), range(len(data)))}
    graph = np.zeros((len(labels),) * 2) + np.inf

    for name, (flow, children) in data.items():
        index = name2index[name]
        indexes = np.array([name2index[i] for i in children])
        graph[index, indexes] = 1

    return graph, labels, flows


def main(data_str):
    graph, labels, flows = parse(data_str)
    N = len(flows)
    # generate_graph_svg(graph, [f"{i} ({f})" for i, f in zip(labels, flows)], "out.svg")

    distances = PyGraph(np.where(np.isinf(graph),0,graph.astype(int))).floyd_warshall()

    flows_cheat = np.where(np.arange(N)==0,flows.max()*10,flows)
    selector = np.arange(N)[(flows_cheat>0)[np.argsort(-flows_cheat)]]

    distances = distances[selector,:][:,selector]
    labels = labels[selector]
    flows = flows[selector]
    
    g = PyGraph(distances)
    for paths in g.iter_paths_by_length():
        raise NotImplementedError
    raise NotImplementedError
