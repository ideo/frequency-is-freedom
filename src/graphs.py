import osmnx as ox
import networkx as nx

from src.filepaths import GRAPH_PATH


def load_chicago_graph():
    chicago = nx.read_gpickle(GRAPH_PATH)
    return chicago


def download_citywide_graph(city="Chicago, Illinois"):
    network_type = "all"
    chicago = ox.graph_from_place(city,
        network_type=network_type,
        retain_all=False,
        truncate_by_edge=True,
        simplify=True)

    chicago = add_walking_times_to_graph(chicago)
    nx.write_gpickle(chicago, GRAPH_PATH)
    print("✓")


def download_graph_from_address(address, radius=2.75, mode="walk"):
    """
    radius (float, int):    
        graph radius in miles
    """
    meters_to_a_mile = 1609
    radius *= meters_to_a_mile

    graph, lat_lng = ox.graph_from_address(address, 
        dist=radius, 
        network_type=mode,
        return_coords=True,
        truncate_by_edge=True,
        simplify=True)
    return graph, lat_lng


def add_walking_times_to_graph(graph, mode="walk"):
    """
    TODO: multiple speeds for multiple kinds of pedestrians
    """
    speeds = {
        "walk": 4.5 #walking speed in km/hr
    }
    meters_per_minute = speeds[mode] * 1000 / 60 #convert to meters/min
    
    for _, _, _, data in graph.edges(data=True, keys=True):
        data['travel_time'] = data['length'] / meters_per_minute
    return graph