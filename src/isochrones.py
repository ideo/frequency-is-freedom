import pickle

import numpy as np
import osmnx as ox
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt

from src.graphs import add_walking_times_to_graph
from src.filepaths import GRAPH_PATH
# from filepaths import DATA_DIR, GRAPH_PATH


class WalkingIsochrone:
    def __init__(self, citywide_graph=None):
        self.citywide_graph = None


    def download_citywide_graph(self, address):
        network_type = "all"
        graph = ox.graph_from_place(address,
            network_type=network_type,
            retain_all=False,
            truncate_by_edge=True,
            simplify=True)

        graph = add_walking_times_to_graph(graph)
        self.citywide_graph = graph



class TransitIsochrone:
    def __init__ (self, 
                  citywide_graph, 
                  stop_id_to_graph_id, 
                  graph_id_to_stop_id, 
                  arrival_rates):
        self.citywide_graph = citywide_graph
        self.stop_id_to_graph_id = stop_id_to_graph_id
        self.graph_id_to_stop_id = graph_id_to_stop_id
        self.arrival_rates = arrival_rates
        self.default_wait_time = np.mean(list(arrival_rates.values()))


    def get_nearest_node(self, location, graph=None):
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
        if graph is None:
            graph = self.citywide_graph

        lat = location[0]
        lng = location[1]
        nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    
        # assert isinstance(nearest_node, int)
        if not isinstance(nearest_node, int):
            nearest_node = nearest_node[0]

        return nearest_node


    def walking_time_to_stop(self, graph, origin_node, dest_node):
        path = ox.distance.shortest_path(graph, origin_node, dest_node, weight="travel_time")
        walking_time = nx.function.path_weight(graph, path, weight="travel_time")
        return walking_time


    def stop_wait_time(self, stop_graph_node):
        stop_id = self.graph_id_to_stop_id[stop_graph_node]
        wait_time = self.arrival_rates.get(stop_id, self.default_wait_time)
        return wait_time


    def determine_remaining_time(self, subgraph, trip_time, origin_node, reachable_nodes):
        walking_time = [self.walking_time_to_stop(subgraph, origin_node, stop_node) for stop_node in reachable_nodes]
        assert all([t > 0 for t in walking_time])

        waiting_time = [self.stop_wait_time(stop_node) for stop_node in reachable_nodes]
        assert all([t > 0 for t in waiting_time])

        remaining_time = [trip_time - walk - wait for walk, wait in zip(walking_time, waiting_time)]
        remaining_time = [time if time > 0 else 0 for time in remaining_time]
        return remaining_time


    def walking_isochrone(self, trip_time, starting_lat_lon=None, starting_node=None):
        """
        From the `starting_lat_lon` the length of the `trip_time` in minutes,
        TKTKTKT
        """
        # Subgraph
        if starting_node is None:
            starting_node = self.get_nearest_node(starting_lat_lon)
        subgraph = nx.ego_graph(self.citywide_graph, starting_node, radius=trip_time, distance='travel_time')
    
        # Reachable Transit Stops 
        transit_stop_graph_ids = set(self.graph_id_to_stop_id.keys())
        reachable_stop_nodes = set(subgraph.nodes).intersection(transit_stop_graph_ids)
        reachable_stop_nodes = list(reachable_stop_nodes)

        # Remaining Travel Time
        remaining_time = self.determine_remaining_time(subgraph, trip_time, starting_node, reachable_stop_nodes)
        return subgraph, reachable_stop_nodes, remaining_time


# def walking_isochrone(citywide_graph, transit_stops, trip_time, starting_lat_lon):
#     """
#     Returns:
#         subgraph (MultiDiGraph)
#             A subset of the citywide graph. The geographic region that is
#             accessible by foot within the `trip_time`
        
#         reachable_stops (list of ints)
#             A list of graph node IDs corresponding to the transit stops 
#             within the subgraph

#         remaining_time (list of floats)
#             A list of how much time is remaining in the `trip_time` after 
#             walking to each transit stop in `reachable_stops`
#     """

#     # Subgraph
#     center_node = center_node = get_nearest_node(citywide_graph, starting_lat_lon)
#     subgraph = nx.ego_graph(citywide_graph, center_node, radius=trip_time, distance='travel_time')
    
#     # Reachable Transit Stops 
#     transit_stop_graph_ids = set(transit_stops["graph_node_id"].values)
#     reachable_stops = set(subgraph.nodes).intersection(transit_stop_graph_ids)
#     reachable_stops = list(reachable_stops)

#     # Remaining Travel Time
#     remaining_time = [trip_time - walking_time_to_stop(subgraph, center_node, stop_node) for stop_node in reachable_stops]
    
#     # Wait for the Bus
    
#     return subgraph, reachable_stops, remaining_time


# def walking_time_to_stop(graph, center_node, transit_stop):
#     path = ox.distance.shortest_path(graph, center_node, transit_stop, weight="travel_time")
#     walking_time = nx.function.path_weight(graph, path, weight="travel_time")
#     return walking_time


# @st.experimental_memo
# def download_graph_from_address(address, radius, mode="walk"):
#     """
#     TODO: We will need to check to see if the the address is in Chicago.
#     --
#     radius (float, int):    
#         graph radius in miles
#     """
#     meters_to_a_mile = 1609
#     radius *= meters_to_a_mile

#     graph, lat_lng = ox.graph_from_address(address, 
#         dist=radius, 
#         network_type=mode,
#         return_coords=True,
#         truncate_by_edge=True,
#         simplify=True)
#     return graph, lat_lng


def load_graph_around_location(location, radius=1609, network_type="walk"):
    """
    location (tuple, list): (lat, lng) of center point
    radius (int): radius in meters (1609 meters is one mile)
    network_type (str): tktk
    """
    graph = ox.graph_from_point(location, 
        dist=radius, 
        network_type=network_type,
        retain_all=False,
        truncate_by_edge=True,
        simplify=True)
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


@st.experimental_memo
def generate_walking_isochrone(location, mode, trip_times, initial_radius=None, _graph=None):
    """
    location (tuple, list):         
        (lat, lng)
    mode (str):                     
        "walk"
    initial_radius (float, int):    
        graph radius in miles
    trip_times (list):              
        travel times to plot
    reachable_node_size (float, int):
        [optional] size of reachable nodes in final plot
    """
    graph = _graph

    # Get the graph
    if graph is None:
        meters_to_a_mile = 1609
        initial_radius *= meters_to_a_mile
        graph = load_graph_around_location(location, radius=initial_radius, network_type=mode)

    # graph = add_travel_time_to_graph_data(graph, mode=mode)
    
    # Set a color scheme
    num_colors = len(trip_times)
    iso_colors = ox.plot.get_colors(num_colors,
        cmap='plasma', 
        start=0, 
        return_hex=True)

    # Color the nodes according to travel time
    center_node = get_nearest_node(graph, location)
    node_colors = {}
    edge_colors = {}
    for trip_time, color in zip(sorted(trip_times, reverse=True), iso_colors):
        subgraph = nx.ego_graph(graph, center_node, radius=trip_time, distance='travel_time')
        for node in subgraph.nodes():
            node_colors[node] = color
        for edge in subgraph.edges():
            edge_colors[edge] = color

    # node color 
    nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
    ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
    
    # node size
    # ns = [reachable_node_size if node in node_colors else 0 for node in graph.nodes()]
    ns = [0 for _ in graph.nodes()]
    
    # Plot
    fig, ax = ox.plot_graph(graph, 
        node_color=nc, node_size=ns, node_alpha=0.8, node_zorder=2,
        edge_color=ec,
        # edge_color='#999999',
        bgcolor='k', edge_linewidth=0.2)

    temp_filename = "plots/isochrone.png"
    plt.savefig(temp_filename, dpi=300, bbox_inches="tight")
    return fig


if __name__ == "__main__":
    # download_citywide_graph()

    chicago = nx.read_gpickle(GRAPH_PATH)

    filepath = DATA_DIR / "stop_id_to_graph_id.pkl"
    with open(filepath, "rb") as pkl_file:
        stop_id_to_graph_id = pickle.load(pkl_file) 
    
    filepath = DATA_DIR / "graph_id_to_stop_id.pkl"
    with open(filepath, "rb") as pkl_file:
        graph_id_to_stop_id = pickle.load(pkl_file)

    filepath = DATA_DIR / "arrival_rates.pkl"
    with open(filepath, "rb") as pkl_file:
        arrival_rates = pickle.load(pkl_file)

    transit_isochrone = TransitIsochrone(
        citywide_graph=chicago,
        stop_id_to_graph_id=stop_id_to_graph_id,
        graph_id_to_stop_id=graph_id_to_stop_id,
        arrival_rates=arrival_rates,
    )

    trip_time = 30
    my_apartment = (41.897999, -87.675908)
    subgraph, reachable_stop_nodes, remaining_time = transit_isochrone.walking_isochrone(trip_time, my_apartment)

    for stp_id, time_left in zip(reachable_stop_nodes, remaining_time):
        print(stp_id, time_left)