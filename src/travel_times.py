from pathlib import Path

import osmnx as ox
import pandas as pd

from isochrones import get_nearest_node


FILEPATH = Path("data/average_travel_times_btwn_stops.csv")


def load_travel_times_dataframe():
    travel_times = pd.read_csv(FILEPATH)
    travel_times.drop(columns=["Unnamed: 0"], inplace=True)
    return travel_times


def find_graph_node_IDs_for_transit_stop():
    # TODO: This didn't work. Perhaps nearest_node returns a list when no one node is the nearest.

    chicago = ox.graph_from_place("Chicago, Illinois")

    travel_times = load_travel_times_dataframe()
    travel_times["graph_node_id"] = travel_times.apply(
        lambda row: get_nearest_node(chicago, [travel_times.stop_lat, travel_times.stop_lon])
    )
    travel_times.to_csv(FILEPATH)


if __name__ == "__main__":
    find_graph_node_IDs_for_transit_stop()