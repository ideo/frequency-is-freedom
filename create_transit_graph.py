import src.gtfs as gtfs
import src.graphs as graphs


def construct_transit_graph_for_requested_date():
    # Data
    routes, trips, stop_times, stops = gtfs.load_clean_and_save_tables()
    citywide_graph = graphs.download_citywide_graph(city="Chicago, Illinois")

    # Bus Frequency
    gtfs.average_arrival_rates_per_stop(stop_times)

    # Match Bus Stops to OSMNX graph
    gtfs.find_graph_node_IDs_for_transit_stop(stops, citywide_graph)

    # Travel Time Between Transit Stops (this takes some time)
    gtfs.average_travel_times_per_route(routes, trips, stop_times)

    # Transit Graph
    gtfs.build_and_save_transit_graph()


if __name__ == "__main__":
    construct_transit_graph_for_requested_date()

    