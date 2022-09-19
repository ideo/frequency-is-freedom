import os
import pickle
import warnings

import osmnx as ox
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm

from src.utils import timer_func
from src.filepaths import DATA_DIR, GTFS_PATH


warnings.filterwarnings("ignore")


GTFS_DTYPES = {
    "trips":    {
        "service_id":   str,
        "trip_id":      str,
        "shape_id":     str,
        "schd_trip_id": str,
    },
    "stop_times":   {
        "trip_id":      str,
    },
    "calendar":     {
        "service_id":   str,
    }
}


class TransitGraph:
    def __init__(self, gtfs_directory, app_data_directory, gtfs_dtypes=GTFS_DTYPES):
        self.gtfs_directory = gtfs_directory
        self.app_data_directory = app_data_directory
        # self.service_date = service_date
        self.gtfs_dtypes = gtfs_dtypes


    ####################### Process Raw GTFS Data #######################

    def load_clean_and_save_tables(self):
 
        print("Loading and cleaning raw GTFS tables.")
        # Load
        trips = load_raw_gtfs_table("trips")
        stop_times = load_raw_gtfs_table("stop_times")
        stops = load_raw_gtfs_table("stops")
        routes = load_raw_gtfs_table("routes")
        calendar = load_raw_gtfs_table("calendar")

        # Filter & Clean
        trips, stop_times = self.filter_by_service_date(calendar, trips, stop_times)
        stop_times = self.convert_datetime_cols(stop_times)
        
        # Save
        save_prepared_gtfs_table(trips, "trips")
        save_prepared_gtfs_table(stop_times, "stop_times")
        save_prepared_gtfs_table(stops, "stops")
        save_prepared_gtfs_table(routes, "routes")


    def load_raw_gtfs_table(self, table_name):
        # print(f"loading table {table_name}")
        filepath = self.gtfs_directory / f"{table_name}.txt"
        if table_name in self.gtfs_dtypes:
            dtype = self.gtfs_dtypes[table_name]
        else:
            dtype = None
        df = pd.read_csv(filepath, dtype=dtype)
        return df


    def save_prepared_gtfs_table(self, df, table_name):
        # TODO Check to see if dir "gtfs_cleaned/" exists. If not, make it

        filepath = self.app_data_directory / "gtfs_cleaned" / f"{table_name}.pkl"
        with open(filepath, "wb") as pkl_file:
                pickle.dump(df, pkl_file)
        print("✓")


    def convert_datetime_cols(self, df):
        """
        Expects only the stop_times table
        """
        hour_of_arrival = lambda ts: int(ts.split(":")[0])
        df["hour_of_arrival"] = df["arrival_time"].apply(hour_of_arrival)

        # Filter to after 6 am and before 10 pm.
        df = df[(df["hour_of_arrival"] >= 5) & (df["hour_of_arrival"] < 22)]

        # Convert to datetime
        frmt = "%H:%M:%S"
        df["arrival_time"] = pd.to_datetime(df["arrival_time"], format=frmt)
        df["departure_time"] = pd.to_datetime(df["departure_time"], format=frmt)
        return df


    def filter_by_service_date(self, calendar, trips, stop_times):
        # TODO:
        # 1. convert datetime column
        # 2. Create day of week columns?
        # 3. Filter

        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        calendar["all_weekdays"] = calendar[weekdays].sum(axis=1) == 5

        # Weekday Service starting Aug. 15th
        wkdy_service = calendar[calendar["all_weekdays"]]
        wkdy_service = wkdy_service[wkdy_service["start_date"] == 20220815]

        # Filter trips and stop_times tables
        service_ids_to_include = wkdy_service["service_id"].values
        trips_filtered = trips[trips["service_id"].isin(service_ids_to_include)]
        trips_ids = trips_filtered["trip_id"].values
        stop_times_filtered = stop_times[stop_times["trip_id"].isin(trips_ids)]
        return trips_filtered, stop_times_filtered



############################# Load & Clean Data #############################



def load_clean_and_save_tables():
    print("Loading and cleaning raw GTFS tables.")
    # Load
    trips = load_raw_gtfs_table("trips")
    stop_times = load_raw_gtfs_table("stop_times")
    stops = load_raw_gtfs_table("stops")
    routes = load_raw_gtfs_table("routes")
    calendar = load_raw_gtfs_table("calendar")

    # Filter & Clean
    trips, stop_times = filter_to_weekday_servive(calendar, trips, stop_times)
    stop_times = clean_stop_times_table(stop_times)
    
    # Save
    save_prepared_gtfs_table(trips, "trips")
    save_prepared_gtfs_table(stop_times, "stop_times")
    save_prepared_gtfs_table(stops, "stops")
    save_prepared_gtfs_table(routes, "routes")


def load_raw_gtfs_table(table_name):
    # print(f"loading table {table_name}")
    filepath = GTFS_PATH / f"{table_name}.txt"
    if table_name in GTFS_DTYPES:
        dtype = GTFS_DTYPES[table_name]
    else:
        dtype = None
    df = pd.read_csv(filepath, dtype=dtype)
    return df


def save_prepared_gtfs_table(df, table_name):
    filepath = DATA_DIR / "gtfs_cleaned" / f"{table_name}.pkl"
    with open(filepath, "wb") as pkl_file:
            pickle.dump(df, pkl_file)
    print("✓")


def load_prepared_gtfs_table(table_name):
    filepath = DATA_DIR / "gtfs_cleaned" / f"{table_name}.pkl"
    with open(filepath, "rb") as pkl_file:
        df = pickle.load(pkl_file)
    return df


def clean_stop_times_table(df):
    df["hour_of_arrival"] = df["arrival_time"].apply(lambda ts: int(ts.split(":")[0]))

    # Filter to after 6 am and before 10 pm.
    df = df[(df["hour_of_arrival"] >= 5) & (df["hour_of_arrival"] < 22)]

    # Convert to datetime
    _format = "%H:%M:%S"
    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format=_format)
    df["departure_time"] = pd.to_datetime(df["departure_time"], format=_format)
    return df


def filter_to_weekday_servive(calendar, trips, stop_times):
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    calendar["all_weekdays"] = calendar[weekdays].sum(axis=1) == 5

    # Weekday Service starting Aug. 15th
    wkdy_service = calendar[calendar["all_weekdays"]]
    wkdy_service = wkdy_service[wkdy_service["start_date"] == 20220815]

    # Filter trips and stop_times tables
    service_ids_to_include = wkdy_service["service_id"].values
    trips_filtered = trips[trips["service_id"].isin(service_ids_to_include)]
    trips_ids = trips_filtered["trip_id"].values
    stop_times_filtered = stop_times[stop_times["trip_id"].isin(trips_ids)]
    return trips_filtered, stop_times_filtered


# def filter_by_service_id(trips, stop_times):
#     """
#     Need more EDA to determine which Service IDs to include, but for the MVP
#     we'll stick with this one. It's weekday service on 100 our of 136 routes.
#     """
#     # These are both integers and strings.
#     service_ids_to_include = [
#         64901,
#         106901,
#         206901,   # I think this is the Purple Line Express
#     ]
#     service_ids_to_include += [str(_id) for _id in service_ids_to_include]

#     trips_filtered = trips[trips["service_id"].isin(service_ids_to_include)]
#     trips_ids = trips_filtered["trip_id"].values
#     stop_times_filtered = stop_times[stop_times["trip_id"].isin(trips_ids)]
#     return trips_filtered, stop_times_filtered


################################### EDA ###################################

def service_ids_that_visit_at_stop(stop_id, stop_times, trips):
    # All the stop times for this stop
    local_stop_times = stop_times[stop_times["stop_id"] == stop_id]
    local_stop_times_trip_ids = local_stop_times["trip_id"].values

    # One Service ID will encompasses many trips. This makes sense.
    service_ids = trips[trips["trip_id"].isin(local_stop_times_trip_ids)]
    service_ids = service_ids["service_id"]
    service_ids = service_ids.value_counts().index.values
    # service_ids = service_ids.astype(str)
    return service_ids


####################### Prepare Date for Isochrones #######################


def save_isochrone_data(obj, table_name):
    filepath = DATA_DIR / "isochrone" / f"{table_name}"
    with open(filepath, "wb") as pkl_file:
            pickle.dump(obj, pkl_file)
    print("✓")


def load_isochrone_data(filename):
    filepath = DATA_DIR / "isochrone"
    if filename in os.listdir(filepath):
        with open(filepath / filename, "rb") as pkl_file:
            obj = pickle.load(pkl_file)
            return obj
    else:
        return None


def average_travel_times_per_route(routes, trips, stop_times):
    """
    TKTKTK Explain. This is the big one.
    """
    print("Calculating travel times between stops per route.")
    travel_times_per_route = load_isochrone_data("travel_times_per_route.pkl")
    if travel_times_per_route is None:
        travel_times_per_route = {}

    for route_id in routes["route_id"].values:
        if route_id not in travel_times_per_route.keys():
            print(f"Determining travel times for route {route_id}")
            trip_ids = trips[trips["route_id"] == route_id]["trip_id"]
            trip_ids = trip_ids.value_counts().index

            if trip_ids.shape[0] > 0:
                pairwise_dfs = []
                for trip_id in tqdm(trip_ids):
                    single_trip = stop_times[stop_times["trip_id"] == trip_id]

                    # Remove duplicated stop IDs
                    # Because why are there repeated stop IDs??
                    single_trip.drop_duplicates(subset=["stop_id"], keep="first", inplace=True)

                    if single_trip.shape[0]:
                        df = single_trip_pairwise_travel_times(single_trip)
                        pairwise_dfs.append(df)

                if pairwise_dfs:
                    average_travel_times = pd.concat(pairwise_dfs).groupby(level=0).mean()
                    travel_times_per_route[route_id] = average_travel_times
                    save_isochrone_data(
                        travel_times_per_route, 
                        "travel_times_per_route.pkl")
                else:
                    print(f"No Stop Times for Trip IDs for route {route_id} in cleaned data.")
            else:
                print(f"No trips for route {route_id} in cleaned data.")
    print("✓")


def single_trip_pairwise_travel_times(df):
    """Compute pairwise travel times between stops for a single trip"""
    df = df.sort_values(by="stop_sequence")
    pairwise_td = df['arrival_time'].values[:, None] - df['arrival_time'].values
    
    to_minutes = lambda td: td / np.timedelta64(1, 'm')
    pairwise_minutes = np.array(list(map(to_minutes, pairwise_td)))
    
    pairwise_df = pd.DataFrame(pairwise_minutes, index=df["stop_id"], columns=df["stop_id"])
    pairwise_df.index.name = "Destination Stop"
    pairwise_df = pairwise_df[pairwise_df > 0]
    return pairwise_df


def average_arrival_rates_per_stop(stop_times):
    """
    To calculate the average arrival rates of buses and trains, we simply count 
    the number of buses/trains per hour, take the average, then the inverse.
    """
    print("Calculating average arrival frequencies for buses and trains.")
    # Buses per Hour
    df = stop_times.groupby(["stop_id","hour_of_arrival"])[["trip_id"]].count()
    df = df.reset_index().groupby("stop_id")[["trip_id"]].mean()

    # Minutes per Bus
    df = df.rename(columns={"trip_id": "average_buses_per_hour"})
    df["avg_minutes_btwn_buses"] = 60/df["average_buses_per_hour"]

    # Convert to dictionary
    stops_ids = df.index.values
    rates = df["avg_minutes_btwn_buses"].values
    arrival_rates = {_id:rate for _id, rate in zip(stops_ids, rates)}

    save_isochrone_data(arrival_rates, "average_arrival_rates_per_stop.pkl")


def find_graph_node_IDs_for_transit_stop(stops, citywide_graph):
    """
    We don't need to put the transit stops on the map, we simply need to find
    the graph node closest to each stop. For our purposes, they don't even need 
    to be exact. The graph is detailed enough that the closest node will be 
    plenty close.
    """
    print("Maping transit stop IDs to graph node IDs.")
    lats = stops["stop_lat"].values
    lons = stops["stop_lon"].values
    graph_nodes = ox.distance.nearest_nodes(citywide_graph, lons, lats)
    graph_nodes = [node if isinstance(node, int) else node[0] for node in graph_nodes]

    stop_ids = stops["stop_id"].values
    stop_id_to_graph_id = {s_id:g_id for s_id, g_id in zip(stop_ids, graph_nodes)}
    graph_id_to_stop_id = {g_id:s_id for s_id, g_id in zip(stop_ids, graph_nodes)}

    save_isochrone_data(stop_id_to_graph_id, "stop_id_to_graph_id.pkl")
    save_isochrone_data(graph_id_to_stop_id, "graph_id_to_stop_id.pkl")


############################### Transit Graph ###############################

@timer_func
def build_transit_graph():
    print("Loading Data")
    stop_id_to_graph_id = load_isochrone_data("stop_id_to_graph_id.pkl")
    average_arrival_rates_per_stop = load_isochrone_data("average_arrival_rates_per_stop.pkl")
    travel_times_per_route = load_isochrone_data("travel_times_per_route.pkl")

    # Concatenate Route Pairwise Travel Times
    print("Concatenating DataFrames")
    full_pairwise_df = pd.concat(list(travel_times_per_route.values()))
    full_pairwise_df = full_pairwise_df.groupby(level=0).min()

    # Label properly and stack
    print("Stacking")
    full_pairwise_df.index.name = "Destination Node"
    full_pairwise_df.columns.name = "Origin Node"
    stacked = pd.DataFrame(full_pairwise_df.T.stack()).reset_index().dropna()
    stacked.rename(columns={0: "transit_travel_time"}, inplace=True)

    # Build the graph
    print("Building the graph")
    graph = nx.from_pandas_edgelist(stacked, 
        source="Origin Node", 
        target="Destination Node", 
        edge_attr="transit_travel_time",
        create_using=nx.DiGraph)

    # Wait times
    print("Adding in Wait Times")
    for edge in graph.edges(data=True):
        origin_node = edge[0]
        edge[2]['wait_time'] = average_arrival_rates_per_stop[origin_node]

    # Index by graph node not Stop ID
    graph = nx.relabel_nodes(graph, stop_id_to_graph_id)

    save_isochrone_data(graph, "transit_graph.pkl")


# @timer_func
# def build_transit_graph():
#     print("Loading Data")
#     stop_id_to_graph_id = load_isochrone_data("stop_id_to_graph_id.pkl")
#     average_arrival_rates_per_stop = load_isochrone_data("average_arrival_rates_per_stop.pkl")
#     travel_times_per_route = load_isochrone_data("travel_times_per_route.pkl")

#     # Concatenate Route Pairwise Travel Times
#     print("Concatenating DataFrames")
#     time_btwn_stops = pd.concat(list(travel_times_per_route.values()))
#     time_btwn_stops = time_btwn_stops.groupby(level=0).min()

#     print("Building the graph")
#     graph = nx.from_pandas_adjacency(time_btwn_stops)
    
#     print("Removing Invalid Edges")
#     edges_to_remove = [edge for edge in graph.edges(data=True) if np.isnan(edge[2]["weight"])]
#     graph.remove_edges_from(edges_to_remove)

#     # Add Wait Times
#     for orig_node in graph:
#         for dest_node in graph[orig_node]:
#             graph[orig_node][dest_node]["weight"] += average_arrival_rates_per_stop[orig_node]

#     # Relabel Graph
#     graph = nx.relabel_nodes(graph, stop_id_to_graph_id)

#     save_isochrone_data(graph, "transit_graph.pkl")
#     print("Done ✓")
#     return graph