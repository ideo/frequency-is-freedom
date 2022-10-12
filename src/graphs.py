import os

import osmnx as ox
import networkx as nx
import streamlit as st

from src.filepaths import DATA_DIR


def graph_path(city):
    filename = city.replace(",", "").replace(" ","_").lower() + ".pkl"
    graph_path = DATA_DIR / filename
    return graph_path


def load_citywide_graph(city):
    citywide_graph = nx.read_gpickle(graph_path(city))
    return citywide_graph


def download_citywide_graph(city="Chicago, Illinois"):
    if os.path.exists(graph_path(city)):
        citywide_graph = load_citywide_graph(city)

    else:
        print("Downloading the citywide network graph")
        network_type = "walk"
        citywide_graph = ox.graph_from_place(city,
            network_type=network_type,
            retain_all=False,
            truncate_by_edge=True,
            simplify=True)

        citywide_graph = add_walking_times_to_graph(citywide_graph)
        nx.write_gpickle(citywide_graph, graph_path(city))
        print(f"✓\tSaved citywide graph to {graph_path(city)}")
    return citywide_graph


@st.experimental_memo
def download_graph_from_address(address, radius=4.5, mode="walk"):
    """
    radius (float, int):    
        graph radius in miles
    """
    print("Downloading graph")
    # meters_to_a_mile = 1609
    radius *= 1000  #conver to meters

    graph, lat_lng = ox.graph_from_address(address, 
        dist=radius, 
        network_type=mode,
        return_coords=True,
        truncate_by_edge=True,
        simplify=True)
    print("✓")
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


def get_nearest_node(graph, location):
    """
    Used to find the center node of the graph. If there is no one closest node, 
    osmnx returns a list. Here we simply take the first node from that list. 
    All the nodes will be right on top of each other and there's no point for 
    our purposes in distinguishing between them.
    ---
    Reminder: Longitude is along the X axis. Latitude is along the Y axis. When 
    we speak we tend to say "lat long", implying latitude comes first. But 
    since latitude goes north/south and longidtude goes east/west, in an X-Y 
    coordinate system, longitude comes first. 
    """
    lat = location[0]
    lng = location[1]
    nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    
    # assert isinstance(nearest_node, int)
    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]

    return nearest_node


# def load_graph_around_location(location, radius=1609, network_type="walk"):
#     """
#     location (tuple, list): (lat, lng) of center point
#     radius (int): radius in meters (1609 meters is one mile)
#     network_type (str): tktk
#     """
#     graph = ox.graph_from_point(location, 
#         dist=radius, 
#         network_type=network_type,
#         retain_all=False,
#         truncate_by_edge=True,
#         simplify=True)
#     return graph