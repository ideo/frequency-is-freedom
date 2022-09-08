import osmnx as ox


def plot_subgraph(graph, nodes_to_color=[]):
    nc = ["#FFFFFF" if node_id not in nodes_to_color else "#0000FF" for node_id in graph.nodes()]
    ox.plot_graph(graph, node_color=nc)