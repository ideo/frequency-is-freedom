import osmnx as ox
import matplotlib.pyplot as plt


def plot_subgraph(graph, nodes_to_color=[]):
    nc = ["#FFFFFF" if node_id not in nodes_to_color else "#0000FF" for node_id in graph.nodes()]
    ox.plot_graph(graph, node_color=nc)


def bus_arrivals_per_hour(stops, trips, stop_times, stop_id, route_code=None):
    stop_desc = stops[stops["stop_id"] == stop_id]["stop_desc"].iloc[0]
    stop_name = stop_desc.split(",")[0].strip()
    direction = stop_desc.split(",")[1].strip()
    
    if route_code is not None:
        trip_ids = trips[trips["route_id"] == route_code]["trip_id"].values
        route_stop_times = stop_times[stop_times["trip_id"].isin(trip_ids)]
    else:
        route_stop_times = stop_times
    
    fig, ax = plt.subplots()
    route_stop_times[route_stop_times["stop_id"] == stop_id]["hour_of_arrival"] \
        .value_counts().sort_index().plot.bar(ax=ax)
    ax.set_title(f"How often does the bus come?\n\nBus Arrivals per Hour\n{stop_name} {direction} stop")
    ax.set_ylabel("No. Buses Arriving")
    ax.set_xlabel("Hour of Arrival")
    plt.xticks(rotation=0);
    return fig