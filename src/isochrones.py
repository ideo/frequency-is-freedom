# import pickle
from time import time

import numpy as np
import pandas as pd
import osmnx as ox
import networkx as nx
from tqdm import tqdm

# import streamlit as st
# import matplotlib.pyplot as plt

import src.graphs as graphs
import src.gtfs as gtfs
# from src.graphs import add_walking_times_to_graph
# from src.filepaths import GRAPH_PATH, DATA_DIR


class WalkingIsochrone:
    def __init__(self, citywide_graph=None):
        self.citywide_graph = None
        
        # TODO: calculate this by finding the center of the provided graph
        self.starting_lat_long = None


    def download_citywide_graph(self, address):
        network_type = "all"
        graph = ox.graph_from_place(address,
            network_type=network_type,
            retain_all=False,
            truncate_by_edge=True,
            simplify=True)

        graph = graphs.add_walking_times_to_graph(graph)
        self.citywide_graph = graph


    def make_isochrone(self, starting_lat_lon, trip_times=None, filepath=None):
        """A Walking Only Isochrone"""
        if trip_times is None:
            trip_times = [15, 30, 45, 60]

        # Set a color scheme
        num_colors = len(trip_times)
        iso_colors = ox.plot.get_colors(num_colors,
            cmap='plasma', 
            start=0, 
            return_hex=True)

        # Node closest to starting address
        starting_node = graphs.get_nearest_node(
            self.citywide_graph, 
            starting_lat_lon)

        # Make subgraphs and color each by trip time
        node_colors = {}
        edge_colors = {}
        trip_times = sorted(trip_times, reverse=True)
        furthest_walking_graph = None
        for trip_time, color in zip(trip_times, iso_colors):
            subgraph = self.make_subgraph(starting_node, trip_time)
            for node in subgraph.nodes():
                node_colors[node] = color
            for edge in subgraph.edges():
                edge_colors[edge] = color
            if furthest_walking_graph is None:
                furthest_walking_graph = subgraph

        # Plot Colors
        # graph = self.citywide_graph
        graph = furthest_walking_graph
        nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
        ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]

        # Node Size
        ns = [0 for _ in graph.nodes()]

        # Plot
        if filepath is None:
            filepath = "plots/user_isochrone.png"

        fig, ax = ox.plot_graph(graph, 
            node_color=nc, edge_color=ec, node_size=ns,
            node_alpha=0.8, node_zorder=2, bgcolor='k', edge_linewidth=0.2,
            show=False, save=True, filepath=filepath, dpi=300)

        return fig
        

    def make_subgraph(self, starting_node, trip_time):
        subgraph = nx.ego_graph(
            self.citywide_graph, 
            starting_node, 
            radius=trip_time, 
            distance='travel_time')
        return subgraph



class TransitIsochrone:
    def __init__ (self, frequency_multiplier=1.0):
        """
        TKTK
        """
        self.frequency_multiplier = frequency_multiplier
        self.load_data_files()
        self.transform_data()


    def load_data_files(self):
        print("Loading Data")
        self.citywide_graph = graphs.load_chicago_graph()

        isochrone_data_files = [
            "stop_id_to_graph_id.pkl",
            "graph_id_to_stop_id.pkl",
            "average_arrival_rates_per_stop.pkl",
            "travel_times_per_route.pkl",
        ]

        for filename in isochrone_data_files:
            attr_name = filename.split(".")[0]
            setattr(self, attr_name, gtfs.load_isochrone_data(filename))


    def transform_data(self):
        # Frequency Update
        # self.average_arrival_rates_per_stop.update(
        #     (stop, wait_time*self.frequency_multiplier) for stop, wait_time
        #     in self.average_arrival_rates_per_stop.items()
        # )

        # Default Wait Time
        avg_wait = np.mean(list(self.average_arrival_rates_per_stop.values()))
        self.default_wait_time = avg_wait

        # Conctentate Route Pairwise Travel Times
        self.time_btwn_stops = pd.concat(
            list(self.travel_times_per_route.values())
        ).groupby(level=0).min()
        print("✓")


    def make_frequency_isochrones(self, starting_lat_lon, trip_time=45, filepath=None):

        frequency_multipliers = [0.5, 1.0, 1.5, 2.0]

        # Set a color scheme
        num_colors = len(frequency_multipliers)
        iso_colors = ox.plot.get_colors(num_colors,
            cmap='plasma', 
            start=0, 
            return_hex=True)

        isochrones = {}
        for frequency_multiplier in frequency_multipliers:
            self.frequency_multiplier = frequency_multiplier
            isochrones[frequency_multiplier] = self.transit_isochrone(trip_time, starting_lat_lon)

        # Color Subgraphs by Frequency Multiplier
        # frequency_multipliers = sorted(frequency_multipliers, reverse=True)
        frequency_multipliers = sorted(frequency_multipliers, reverse=False)
        node_colors = {}
        edge_colors = {}
        for freq, color in zip(frequency_multipliers, iso_colors):
            subgraph = isochrones[freq]
            for node in subgraph.nodes():
                node_colors[node] = color
            for edge in subgraph.edges():
                edge_colors[edge] = color

        graph = nx.compose_all(isochrones.values())
        nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
        ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
        ns = [0 for _ in graph.nodes()]

        # Plot
        if filepath is None:
            filepath = f"plots/frequency_isochrone_{trip_time}_minute_trip.png"

        fig, ax = ox.plot_graph(graph, 
            node_color=nc, edge_color=ec, node_size=ns,
            node_alpha=0.8, node_zorder=2, bgcolor='k', edge_linewidth=0.2,
            show=False, save=True, filepath=filepath, dpi=300)



    def make_isochrone(self, starting_lat_lon, trip_times=None, filepath=None):
        """A Walking and Transit Isochrone!!"""
        if trip_times is None:
            trip_times = [15, 30, 45, 60]

        # Set a color scheme
        num_colors = len(trip_times)
        iso_colors = ox.plot.get_colors(num_colors,
            cmap='plasma', 
            start=0, 
            return_hex=True)

        isochrones = {}
        for trip_time in trip_times:
            isochrones[trip_time] = self.transit_isochrone(trip_time, starting_lat_lon)

        # Color Subgraphs by Trip Time
        trip_times = sorted(trip_times, reverse=True)
        node_colors = {}
        edge_colors = {}
        for trip_time, color in zip(trip_times, iso_colors):
            subgraph = isochrones[trip_time]
            for node in subgraph.nodes():
                node_colors[node] = color
            for edge in subgraph.edges():
                edge_colors[edge] = color

        graph = nx.compose_all(isochrones.values())
        nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
        ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
        ns = [0 for _ in graph.nodes()]

        # Plot
        if filepath is None:
            filepath = "plots/user_transit_isochrone.png"

        fig, ax = ox.plot_graph(graph, 
            node_color=nc, edge_color=ec, node_size=ns,
            node_alpha=0.8, node_zorder=2, bgcolor='k', edge_linewidth=0.2,
            show=False, save=True, filepath=filepath, dpi=300)

        return fig


    def transit_isochrone(self, trip_time, lat_lon=None):
        """
        TKTK
        """
        print(f"Calculating transit isochrone for a {trip_time} minute trip time.")
        starting_node = self.get_nearest_node(lat_lon)
        self.start_positions = {}
        self.missing_stops = []
        self.subgraphs = []

        graph = self.walking_subgraph(starting_node, trip_time)
        _ = self.walking_subgraph(starting_node, trip_time)
        graph = nx.compose_all(self.subgraphs)
        return graph


    def walking_subgraph(self, starting_node, trip_time, isochrone_graph=None):
        """
        Generates a subgraph of everywere you can walk from either `starting_node`
        or `lat_lon` within the `trip_time`.

        Returns the subgraph, and a list of all transit stops with the subgraph
        and how much trip time is left after walking to them.
        """
        # Subgraph
        subgraph = nx.ego_graph(self.citywide_graph, starting_node, 
            radius=trip_time, 
            distance='travel_time')
        self.subgraphs.append(subgraph)

        if isochrone_graph is None:
            isochrone_graph = subgraph
        # isochrone_graph = nx.compose(isochrone_graph, subgraph)
    
        # Reachable Transit Stops 
        transit_stop_graph_ids = set(self.graph_id_to_stop_id.keys())
        reachable_stop_nodes = set(subgraph.nodes).intersection(transit_stop_graph_ids)
        reachable_stop_nodes = list(reachable_stop_nodes)

        # Remaining Travel Time
        remaining_time = self.determine_remaining_time(subgraph, trip_time, starting_node, reachable_stop_nodes)

        # Stops we can travel from
        transit_stops = [(stop_node, time_left) for stop_node, time_left in 
            zip(reachable_stop_nodes, remaining_time) if time_left > 0]
        transit_stops = sorted(transit_stops, key=lambda x: x[1], reverse=True)

        # New Starting Nodes and Trip Times
        new_start_nodes_and_travel_times = [
            self.new_start_positions(stop_node, time_left) 
                for stop_node, time_left in transit_stops]   
        new_start_nodes_and_travel_times = [start_pair for start_pair in new_start_nodes_and_travel_times if start_pair]

        # Recursion, baby!
        # if new_start_nodes_and_travel_times:
        for transit_stop in new_start_nodes_and_travel_times:
            for starting_node, trip_time in transit_stop:
                # print(starting_node, trip_time)
                # return self.walking_subgraph(starting_node, trip_time, isochrone_graph)
                self.walking_subgraph(starting_node, trip_time, isochrone_graph)
                # isochrone_graph = nx.compose(
                #     isochrone_graph,
                #     self.walking_subgraph(starting_node, trip_time, isochrone_graph)
                # )
        
        # return isochrone_graph


    def new_start_positions(self, origin_graph_node, remaining_time):
        """
        Other transit stops we can travel to with however much time is left.

        Returns a list of Graph Node IDs and how much time is left to travel 
        after we travel there.
        """
        origin_stop_id = self.graph_id_to_stop_id[origin_graph_node]

        # Based on how we filter service, we may not have travel times
        # for all reachable stops
        if origin_stop_id not in self.time_btwn_stops.index:
            self.missing_stops.append(origin_stop_id)
            return []

        travel_times = self.time_btwn_stops.loc[:, origin_stop_id].dropna()

        # Time left after traveling there
        travel_times = travel_times[travel_times <= remaining_time]
        travel_times = remaining_time - travel_times

        # Convert to a dictionary
        travel_times.sort_values(ascending=False, inplace=True)
        travel_times = travel_times.to_dict()

        # Stop IDs to graph nodes
        starting_nodes_and_trip_times = [
            (self.stop_id_to_graph_id[stop_id], time_left) for stop_id, 
            time_left in travel_times.items()]

        # Don't revisit stops
        starting_nodes_and_trip_times = [(graph_node, trip_time) for 
            graph_node, trip_time in starting_nodes_and_trip_times 
            if not self.previously_visited_this_stop(graph_node, trip_time)]

        return starting_nodes_and_trip_times


    def previously_visited_this_stop(self, graph_node, trip_time):
        """
        To prevent us from riding the bus back and forth
        """
        if graph_node not in self.start_positions:
            self.start_positions[graph_node] = trip_time
            return False

        else:
            if trip_time > self.start_positions[graph_node]:
                self.start_positions[graph_node] = trip_time
                return False
        
        return True


    def get_nearest_node(self, location, graph=None, trip_times=None):
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
    
        if not isinstance(nearest_node, int):
            nearest_node = nearest_node[0]

        return nearest_node


    def walking_time_to_stop(self, graph, origin_node, dest_node):
        path = ox.distance.shortest_path(graph, origin_node, dest_node, weight="travel_time")
        walking_time = nx.function.path_weight(graph, path, weight="travel_time")
        return walking_time


    def stop_wait_time(self, stop_graph_node):
        stop_id = self.graph_id_to_stop_id[stop_graph_node]
        wait_time = self.average_arrival_rates_per_stop.get(stop_id, self.default_wait_time)
        wait_time = wait_time / self.frequency_multiplier
        return wait_time


    def determine_remaining_time(self, subgraph, trip_time, origin_node, reachable_nodes):
        walking_time = [self.walking_time_to_stop(subgraph, origin_node, stop_node) for stop_node in reachable_nodes]
        assert all([t >= 0 for t in walking_time])

        waiting_time = [self.stop_wait_time(stop_node) for stop_node in reachable_nodes]
        assert all([t > 0 for t in waiting_time])

        remaining_time = [trip_time - walk - wait for walk, wait in zip(walking_time, waiting_time)]
        remaining_time = [time if time > 0 else 0 for time in remaining_time]
        return remaining_time


def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


if __name__ == '__main__':
    pass


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


# def get_nearest_node(graph, location):
#     """
#     Used to find the center node of the graph. If there is no one closest node, 
#     osmnx returns a list. Here we simply take the first node from that list. 
#     All the nodes will be right on top of each other and there's no point for 
#     our purposes in distinguishing between them.
#     ---
#     Reminder: Longitude is along the X axis. Latitude is along the Y axis. When 
#     we speak we tend to say "lat long", implying latitude comes first. But 
#     since latitude goes north/south and longidtude goes east/west, in an X-Y 
#     coordinate system, longitude comes first. 
#     """
#     lat = location[0]
#     lng = location[1]
#     nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    
#     # assert isinstance(nearest_node, int)
#     if not isinstance(nearest_node, int):
#         nearest_node = nearest_node[0]

#     return nearest_node


# @st.experimental_memo
# def generate_walking_isochrone(location, mode, trip_times, initial_radius=None, _graph=None):
#     """
#     location (tuple, list):         
#         (lat, lng)
#     mode (str):                     
#         "walk"
#     initial_radius (float, int):    
#         graph radius in miles
#     trip_times (list):              
#         travel times to plot
#     reachable_node_size (float, int):
#         [optional] size of reachable nodes in final plot
#     """
#     graph = _graph

#     # Get the graph
#     if graph is None:
#         meters_to_a_mile = 1609
#         initial_radius *= meters_to_a_mile
#         graph = load_graph_around_location(location, radius=initial_radius, network_type=mode)

#     # graph = add_travel_time_to_graph_data(graph, mode=mode)
    
#     # Set a color scheme
#     num_colors = len(trip_times)
#     iso_colors = ox.plot.get_colors(num_colors,
#         cmap='plasma', 
#         start=0, 
#         return_hex=True)

#     # Color the nodes according to travel time
#     center_node = graphs.get_nearest_node(graph, location)
#     node_colors = {}
#     edge_colors = {}
#     for trip_time, color in zip(sorted(trip_times, reverse=True), iso_colors):
#         subgraph = nx.ego_graph(graph, center_node, radius=trip_time, distance='travel_time')
#         for node in subgraph.nodes():
#             node_colors[node] = color
#         for edge in subgraph.edges():
#             edge_colors[edge] = color

#     # node color 
#     nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
#     ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
    
#     # node size
#     # ns = [reachable_node_size if node in node_colors else 0 for node in graph.nodes()]
#     ns = [0 for _ in graph.nodes()]
    
#     # Plot
#     fig, ax = ox.plot_graph(graph, 
#         node_color=nc, node_size=ns, node_alpha=0.8, node_zorder=2,
#         edge_color=ec,
#         # edge_color='#999999',
#         bgcolor='k', edge_linewidth=0.2)

#     temp_filename = "plots/isochrone.png"
#     plt.savefig(temp_filename, dpi=300, bbox_inches="tight")
#     return fig
