import matplotlib.pyplot as plt

import src.graphs as graphs
from src.isochrones import WalkingIsochrone, TransitIsochrone, timer_func
from src.filepaths import DATA_DIR


@timer_func
def walking_isochrone_from_my_apartment():
    print("Generating the Walking Isochrone")
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    city = "Chicago, Illinois"
    graph = graphs.load_citywide_graph(city)
    walking_isochrone = WalkingIsochrone(graph)
    filepath = "plots/walking_isochrone_from_my_apartment.png"
    walking_isochrone.make_isochrone(my_lat_lon, filepath=filepath)


@timer_func
def transit_isochrone_from_my_apartment():
    city = "Chicago, Illinois"
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    transit_isochrone = TransitIsochrone(DATA_DIR, city)

    trip_times = [15, 30, 45, 60]
    freq_multipliers = [1]
    filepath = "plots/transit_isochrone_from_my_apartment.png"
    transit_isochrone.make_isochrone(my_lat_lon, trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        cmap="plasma")


@timer_func
def frequency_isochrones_from_my_apartment(trip_time=30):
    city = "Chicago, Illinois"
    my_lat_lon = (41.898010150000005, -87.67613740698785)
    transit_isochrone = TransitIsochrone(DATA_DIR, city)

    freq_multipliers = [0.5, 1, 2, 3]
    bgcolor="#262730"
    fig, ax = plt.subplots(nrows=1, ncols=len(freq_multipliers), 
        figsize=(3*len(freq_multipliers), 4))

    for ii, freq in enumerate(freq_multipliers):
        filepath = f"plots/frequency_isochrone_{trip_time}_min_trips.png"
        transit_isochrone.make_isochrone(my_lat_lon, 
            trip_times=[trip_time], 
            freq_multipliers=[freq],
            filepath=filepath,
            color="#B3DDF2",
            bgcolor=bgcolor,
            use_city_bounds=True,
            ax=ax[ii])
        plt.savefig(filepath, dpi=300, facecolor=bgcolor)


if __name__ == "__main__":
    walking_isochrone_from_my_apartment()
    transit_isochrone_from_my_apartment()
    frequency_isochrones_from_my_apartment(trip_time=30)
    frequency_isochrones_from_my_apartment(trip_time=45)
    frequency_isochrones_from_my_apartment(trip_time=60)



