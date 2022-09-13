import osmnx as ox

import src.gtfs as gtfs
import src.graphs as graphs
from src.isochrones import WalkingIsochrone, TransitIsochrone, timer_func


def walking_isochrone_from_my_apartment():
    print("Generating the Walking Isochrone")
    my_address = "906 N Winchester Ave, Chicago, IL 60622"
    # Please send me something nice for Christmas

    # TODO: Just take as subgraph of the chicago graph
    graph, starting_lat_lon = graphs.download_graph_from_address(my_address)

    walking_isochrone = WalkingIsochrone()
    walking_isochrone.citywide_graph = graph
    filepath = "plots/walking_isochrone_from_my_apartment.png"
    _ = walking_isochrone.make_isochrone(starting_lat_lon, filepath=filepath)


@timer_func
def transit_isochrone_from_my_apartment():
    my_address = "906 N Winchester Ave, Chicago, IL 60622"
    my_lat_lon = ox.geocoder.geocode(my_address)

    transit_isochrone = TransitIsochrone()
    filepath = "plots/transit_isochrone_from_my_apartment.png"
    transit_isochrone.make_isochrone(my_lat_lon, filepath=filepath)


    # trip_time = 20
    # This took 8 minutes to run.
    # for trip_time in [10, 15, 20, 30, 45]:
    #     graph = transit_isochrone.transit_isochrone(trip_time, my_lat_lon)

    #     filepath = f"plots/transit_isochrone_{trip_time}.png"
    #     fig, ax = ox.plot_graph(graph, 
    #         # node_color=nc, edge_color=ec, node_size=ns,
    #         node_size=0,
    #         node_alpha=0.8, node_zorder=2, bgcolor='k', edge_linewidth=0.2,
    #         show=False, save=True, filepath=filepath, dpi=300)



@timer_func
def frequency_maps():
    my_address = "906 N Winchester Ave, Chicago, IL 60622"
    my_lat_lon = ox.geocoder.geocode(my_address)

    transit_isochrone = TransitIsochrone()
    transit_isochrone.make_frequency_isochrones(my_lat_lon, trip_time=45)


    # for bus_frequency in [0.5, 1.0, 2.0]:
    #     trip_times = [30]
    #     transit_isochrone = TransitIsochrone(frequency_multiplier=bus_frequency)

    #     filepath = f"plots/transit_isochrone_{trip_times[0]}_trip_at_{bus_frequency}_time_frequency.png"
    #     transit_isochrone.make_isochrone(my_lat_lon, 
    #         trip_times=trip_times, 
    #         filepath=filepath)



if __name__ == "__main__":
    # Data
    # gtfs.load_clean_and_save_tables()
    # graphs.download_citywide_graph()

    # routes = gtfs.load_prepared_gtfs_table("routes")
    # trips = gtfs.load_prepared_gtfs_table("trips")
    # stop_times = gtfs.load_prepared_gtfs_table("stop_times")  
    # stops = gtfs.load_prepared_gtfs_table("stops") 

    # # # Bus Frequency
    # gtfs.average_arrival_rates_per_stop(stop_times)

    # # Match Bus Stops to OSMNX graph
    # chicago = graphs.load_chicago_graph()
    # gtfs.find_graph_node_IDs_for_transit_stop(stops, chicago)

    # Travel Time Between Transit Stops (this takes some time)
    # gtfs.average_travel_times_per_route(routes, trips, stop_times)

    # Isochrone Images
    # walking_isochrone_from_my_apartment()
    # transit_isochrone_from_my_apartment()
    frequency_maps()



