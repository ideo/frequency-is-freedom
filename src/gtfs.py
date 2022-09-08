from pathlib import Path
import pickle

import osmnx as ox
import pandas as pd
import networkx as nx

from src.filepaths import DATAFRAME_PATH



# def download_chicago():
#     network_type = "all"
#     chicago = ox.graph_from_place("Chicago, Illinois",
#         network_type=network_type,
#         retain_all=False,
#         truncate_by_edge=True,
#         simplify=True)

#     # TODO: Add travel times here
#     nx.write_gpickle(chicago, GRAPH_PATH)
#     print("✓")


def load_travel_times_dataframe():
    travel_times = pd.read_csv(DATAFRAME_PATH)
    travel_times.drop(columns=["Unnamed: 0"], inplace=True)
    return travel_times


def find_graph_node_IDs_for_transit_stop():
    """
    We don't need to put the transit stops on the map, we simply need to find
    the graph node closest to each stop. For our purposes, they don't even need 
    to be exact. The graph is detailed enough that the closest node will be 
    plenty close.
    """
    
    chicago = nx.read_gpickle(GRAPH_PATH)
    travel_times = load_travel_times_dataframe()

    lats = travel_times["stop_lat"].values
    lons = travel_times["stop_lon"].values
    graph_nodes = ox.distance.nearest_nodes(chicago, lons, lats)
    graph_nodes = [node if isinstance(node, int) else node[0] for node in graph_nodes]
    
    travel_times["graph_node_id"] = graph_nodes
    travel_times.to_csv(DATAFRAME_PATH)
    print("✓")


if __name__ == "__main__":
    # download_chicago()
    # find_graph_node_IDs_for_transit_stop()
    pass