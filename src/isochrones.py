import osmnx as ox
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt

from src.filepaths import GRAPH_PATH



def download_citywide_graph(city="Chicago, Illinois"):
    network_type = "all"
    chicago = ox.graph_from_place(city,
        network_type=network_type,
        retain_all=False,
        truncate_by_edge=True,
        simplify=True)

    # TODO: Add travel times here
    nx.write_gpickle(chicago, GRAPH_PATH)
    print("✓")


def get_subgraph_and_reachable_stops(citywide_graph, transit_stops, trip_time, starting_lat_lon):
    # Subgraph
    center_node = center_node = get_nearest_node(citywide_graph, starting_lat_lon)
    subgraph = nx.ego_graph(citywide_graph, center_node, radius=trip_time, distance='travel_time')
    
    # Reachable Transit Stops 
    transit_stop_graph_ids = set(transit_stops["graph_node_id"].values)
    reachable_stops = set(subgraph.nodes).intersection(transit_stop_graph_ids)
    reachable_stops = list(reachable_stops)
    
    return subgraph, reachable_stops


@st.experimental_memo
def download_graph_from_address(address, radius, mode="walk"):
    """
    TODO: We will need to check to see if the the address is in Chicago.
    --
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
    Used to find the center node of the graph.
    ---
    Reminder: Longitude is along the X axis. Latitude is along the Y axis.
    
    When we speak we tend to say "lat long", implying latitude comes first. 
    But since latitude goes north/south and longidtude goes east/west, in 
    an X-Y coordinate system, longitude comes first. 

    TKTK Explain
    """
    lat = location[0]
    lng = location[1]
    nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    
    # assert isinstance(nearest_node, int)
    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]

    print(nearest_node)
    return nearest_node


def add_travel_time_to_graph_data(graph, mode="walk"):
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

    graph = add_travel_time_to_graph_data(graph, mode=mode)
    
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
    pass
    # my_apartment = (41.897999, -87.675908)
    # mode = "walk"
    # initial_radius = 1.5   #miles
    # trip_times = [5, 10, 15, 20, 25]

    # _ = generate_isochrone(my_apartment, mode, initial_radius, trip_times)

    # chicago = nx.read_gpickle(GRAPH_PATH)
    # # travel_times = load_travel_times_dataframe()

    # trip_time = 15 #minutes
    # my_apartment = (41.898010150000005, -87.67613740698785)
    # subgraph, reachable_stops = get_subgraph_and_reachable_stops(
    #     chicago,
    #     travel_times,
    #     trip_time, 
    #     my_apartment
    # )
    # plot_subgraph(subgraph, reachable_stops)