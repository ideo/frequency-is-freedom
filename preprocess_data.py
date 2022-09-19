# import osmnx as ox

# import src.gtfs as gtfs
import src.graphs as graphs
from src.isochrones import WalkingIsochrone, TransitIsochrone, timer_func
from src.filepaths import DATA_DIR


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
    # my_address = "906 N Winchester Ave, Chicago, IL 60622"
    # my_lat_lon = ox.geocoder.geocode(my_address)
    my_lat_lon = (41.898010150000005, -87.67613740698785)

    transit_isochrone = TransitIsochrone(DATA_DIR)

    # trip_times = [15, 30, 45, 60]
    # freq_multipliers = [1]
    # filepath = "plots/transit_isochrone_from_my_apartment.png"
    # transit_isochrone.make_isochrone(my_lat_lon, trip_times=trip_times, 
    #     freq_multipliers=freq_multipliers,
    #     filepath=filepath,
    #     cmap="plasma")

    # trip_times = [60]
    trip_times = [20]
    freq_multipliers = [0.5, 1, 2]
    filepath = f"plots/frequency_isochrone_{trip_times[0]}_min_trip.png"
    transit_isochrone.make_isochrone(my_lat_lon, trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        cmap="viridis")


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

    # Transit Graph
    # graph = gtfs.build_transit_graph()

    # Isochrone Images
    # walking_isochrone_from_my_apartment()
    transit_isochrone_from_my_apartment()
    # frequency_maps()



