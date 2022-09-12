import src.gtfs as gtfs
import src.graphs as graphs


def walking_isochrone_from_my_apartment():
    pass


if __name__ == "__main__":
    gtfs.load_clean_and_save_tables()
    # graphs.download_citywide_graph()

    routes = gtfs.load_prepared_gtfs_table("routes")
    trips = gtfs.load_prepared_gtfs_table("trips")
    stop_times = gtfs.load_prepared_gtfs_table("stop_times")  
    # stops = gtfs.load_prepared_gtfs_table("stops") 

    # Bus Frequency
    gtfs.average_arrival_rates_per_stop(stop_times)

    # Match Bus Stops to OSMNX graph
    # chicago = graphs.load_chicago_graph()
    # gtfs.find_graph_node_IDs_for_transit_stop(stops, chicago)

    # Travel Time Between Transit Stops (this takes some time)
    gtfs.average_travel_times_per_route(routes, trips, stop_times)