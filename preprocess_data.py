from threading import local
import src.gtfs as gtfs
import src.graphs as graphs
from src.isochrones import WalkingIsochrone


def walking_isochrone_from_my_apartment():
    my_address = "906 N Winchester Ave, Chicago, IL 60622"
    # Please send me something nice for Christmas

    # TODO: Just take as subgraph of the chicago graph
    radius = 1.75   #miles
    local_graph, starting_lat_lon = graphs.download_graph_from_address(
        my_address, radius=radius)

    walking_isochrone = WalkingIsochrone()
    walking_isochrone.citywide_graph = local_graph
    filepath = "plots/walking_isochrone_from_my_apartment.png"
    _ = walking_isochrone.make_isochrone(starting_lat_lon, filepath=filepath)


if __name__ == "__main__":
    # Data
    # gtfs.load_clean_and_save_tables()
    # graphs.download_citywide_graph()

    # routes = gtfs.load_prepared_gtfs_table("routes")
    # trips = gtfs.load_prepared_gtfs_table("trips")
    # stop_times = gtfs.load_prepared_gtfs_table("stop_times")  
    # stops = gtfs.load_prepared_gtfs_table("stops") 

    # # Bus Frequency
    # gtfs.average_arrival_rates_per_stop(stop_times)

    # # Match Bus Stops to OSMNX graph
    # chicago = graphs.load_chicago_graph()
    # gtfs.find_graph_node_IDs_for_transit_stop(stops, chicago)

    # # Travel Time Between Transit Stops (this takes some time)
    # gtfs.average_travel_times_per_route(routes, trips, stop_times)

    # Isochrone Images
    walking_isochrone_from_my_apartment()