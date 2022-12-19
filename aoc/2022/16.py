import re
import numpy as np

demo_data="""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

demo_result=1651

matcher = re.compile("Valve ([A-Z]{2}) has flow rate=(-?\d+); tunnels? leads? to valves? ([A-Z, ]+)")

def make_graph(data):
    import graphviz
    dot = graphviz.Digraph()
    for name, (flow,children) in data.items():
        dot.node(name, label= f"{name} ({flow})")
    for name, (flow,children) in data.items():
        for child in children:
            dot.edge(name, child)
    dot.render("graph.svg")
    
def floyd_warshall(graph):
    n = len(graph)

    # Initialise la distance entre chaque paire de sommets à l'infini
    distance = [[float("inf") for _ in range(n)] for _ in range(n)]

    # Initialise la distance entre chaque sommet à 0
    for i in range(n):
        distance[i][i] = 0
    
    # Remplit la matrice de distance en utilisant les valeurs de l'adjacence
    for i in range(n):
        for j in range(n):
            if graph[i][j] != float("inf"):
                distance[i][j] = graph[i][j]

    # Applique l'algorithme de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    return np.array(distance).astype(np.int)
    
def main(data_str):
    data = [[i[0],(i[1],i[2].split(", "))] for i in matcher.findall(data_str)]
    start_point = data[0][0]
    data = dict(data)
    gas_amount = {k:int(v[0]) for k,v in data.items()}
    node_index = {i:j for i,j in zip(data.keys(),range(len(data)))}

    make_graph(data)
    
    links = np.zeros((len(data),len(data)))+np.inf
    for name,(flow, children) in data.items():
        indexes = [node_index[i] for i in children]
        links[node_index[name],np.array(indexes)] = 1
    distances = floyd_warshall(links)
    
    def search(queue):
        while len(queue):
            position, opened, time_left, gas_saved = queue.pop(0)
            flow, children = data[position]
            children = sorted(children,key=lambda x:-int(data[x][0]))
        
            if time_left == 0:
                # compute amount saved
                raise NotImplementedError
            
            released = sum(gas_amount[i] for i in opened)
            for opening in ([True,False] if int(flow)>0 else [False]):
                for child in [i for i in children if i not in opened]:
                    if opening:
                        queue.append((child, opened | {position}, time_left-2, gas_saved+released+gas_amount[position]))
                    else:
                        queue.append((child, opened,time_left-1, gas_saved+released))
            
    res = search([(start_point,set(), 30,0)])
    raise NotImplementedError