import os
import pickle
import warnings

import osmnx as ox
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm

# from filepaths import DATA_DIR, DATAFRAME_PATH, GTFS_PATH, GRAPH_PATH
from src.filepaths import DATA_DIR, DATAFRAME_PATH, GTFS_PATH, GRAPH_PATH


warnings.filterwarnings("ignore")


############################# Load & Clean Data #############################

def load_clean_and_save_tables():
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
    filepath = GTFS_PATH / f"{table_name}.txt"
    df = pd.read_csv(filepath)
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


def enforce_data_types():
    pass


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
    return pairwise_df


def average_arrival_rates_per_stop(stop_times):
    """
    To calculate the average arrival rates of buses and trains, we simply count 
    the number of buses/trains per hour, take the average, then the inverse.
    """
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


# def arrival_frequencies_per_stop():
#     """
#     Eventually, I'd like to disaggregate arrival rates by route ID, but for the
#     MVP we'll lump them together in order to move quickly.
#     """
#     # Data
#     stop_times = load_raw_gtfs_table("stop_times")
#     stop_times = clean_stop_times_table(stop_times)
#     stop_times = stop_times[["trip_id", "stop_id", "arrival_time"]]

#     # Arrival Intervals
#     arrival_rates = stop_times.sort_values(by="arrival_time")
#     arrival_rates = arrival_rates.groupby("stop_id")["arrival_time"].apply(
#         lambda at: np.diff(np.asarray(at)).mean() / np.timedelta64(1, 'm'))
#     arrival_rates = pd.DataFrame(arrival_rates)
#     arrival_rates.rename(columns={"arrival_time": "arrival_rate"}, inplace=True)
    
#     # If done properly, these should all be greater than zero.
#     # TODO: It's not yet, so let's investigate why.
#     negative_values = [r<0 for r in arrival_rates["arrival_rate"].values]
#     if any(negative_values):
#         percent = sum(negative_values) / arrival_rates.shape[0] * 100
#         warnings.warn(f"{round(percent)}% of arrival rates are negative.")

#     # Fix values
#     mask = arrival_rates["arrival_rate"] <= 0
#     arrival_rates.loc[mask, "arrival_rate"] = np.NaN
#     arrival_rates["arrival_rate"].fillna(arrival_rates["arrival_rate"].mean(), 
#         inplace=True)

#     # Convert to dictionary
#     stops_ids = arrival_rates.index.values
#     rates = arrival_rates["arrival_rate"].values
#     arrival_rates = {_id:rate for _id, rate in zip(stops_ids, rates)}

#     # Save
#     filepath = DATA_DIR / "arrival_rates.pkl"
#     with open(filepath, "wb") as pkl_file:
#             pickle.dump(arrival_rates, pkl_file)
#     print("✓")


# def arrival_frequencies_per_stop_per_route():
#     stop_times = load_raw_gtfs_table("stop_times")
#     stop_times = clean_stop_times_table(stop_times)
#     stop_times = stop_times[["trip_id", "stop_id", "arrival_time"]]
    
#     trips = load_raw_gtfs_table("trips")
#     trips = trips[["trip_id", "route_id"]]

#     # When merging these dataframes, many Route IDs are left as NaN
#     # That's very curious
#     arrival_frequencies = stop_times.merge(trips, how="left", on="trip_id")
#     arrival_frequencies["route_id"].fillna(value="unspecified", inplace=True)

#     # Interval Means
#     arrival_frequencies = arrival_frequencies.groupby(
#         ["route_id", "stop_id"])["arrival_time"].apply(
#             lambda at: np.diff(np.asarray(at)).mean() / np.timedelta64(1, 'm'))
    
#     # Impute missing values
#     # assume average bus frequency
#     arrival_frequencies.fillna(value=arrival_frequencies.mean())

#     num_stops = arrival_frequencies.reset_index()["stop_id"].value_counts().shape[0]
#     stops = load_raw_gtfs_table("stops")
#     missing_stops = stops.shape[0] - num_stops
#     print(f"Missing arrival frequencies for {missing_stops} transit stops.")

#     # For now, we will ignore routes in arrival times. We'll figure out how to 
#     # incorporate that later
#     # TODO: Figure out the best way to incorporate routes!
#     arrival_frequencies = arrival_frequencies.reset_index() \
#         .drop(columns="route_id").groupby("stop_id").mean()

#     stops_ids = arrival_frequencies.index.values
#     arrival_rates = arrival_frequencies["arrival_time"].values
#     arrival_frequencies = {_id:rate for _id, rate in zip(stops_ids, arrival_rates)}

#     filepath = DATA_DIR / "arrival_frequencies.pkl"
#     with open(filepath, "wb") as pkl_file:
#             pickle.dump(arrival_frequencies, pkl_file)
#     print("✓")



# def load_travel_times_dataframe():
#     travel_times = pd.read_csv(DATAFRAME_PATH)
#     travel_times.drop(columns=["Unnamed: 0"], inplace=True)
#     return travel_times


def find_graph_node_IDs_for_transit_stop(stops, citywide_graph):
    """
    We don't need to put the transit stops on the map, we simply need to find
    the graph node closest to each stop. For our purposes, they don't even need 
    to be exact. The graph is detailed enough that the closest node will be 
    plenty close.
    """
    lats = stops["stop_lat"].values
    lons = stops["stop_lon"].values
    graph_nodes = ox.distance.nearest_nodes(citywide_graph, lons, lats)
    graph_nodes = [node if isinstance(node, int) else node[0] for node in graph_nodes]

    stop_ids = stops["stop_id"].values
    stop_id_to_graph_id = {s_id:g_id for s_id, g_id in zip(stop_ids, graph_nodes)}
    graph_id_to_stop_id = {g_id:s_id for s_id, g_id in zip(stop_ids, graph_nodes)}

    save_isochrone_data(stop_id_to_graph_id, "stop_id_to_graph_id.pkl")
    save_isochrone_data(graph_id_to_stop_id, "graph_id_to_stop_id.pkl")
    

if __name__ == "__main__":
    pass
    # prepare_needed_data()

    # download_chicago()
    # find_graph_node_IDs_for_transit_stop()
    # average_travel_times_per_route()
    # find_graph_node_IDs_for_transit_stop()
    # arrival_frequencies_per_stop()