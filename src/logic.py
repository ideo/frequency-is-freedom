from zipfile import ZipFile

import osmnx as ox
# import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st

from numpy import random
random = random.RandomState(42)

from .text import TEXT
import src.gtfs as gtfs
import src.graphs as graphs
from src.isochrones import WalkingIsochrone, TransitIsochrone
from src.filepaths import DATA_DIR, FREQUENCY_DIR


################################ App Logic ################################

def write_text(section_title, header_level=3, header=True):
    if header:
        if header_level > 1:
            st.write("")
        header_hashes = "#"*header_level
        st.markdown(f"{header_hashes} {section_title}")
    for paragraph in TEXT[section_title]:
        st.write(paragraph)


def initialize_session_state():
    initial_values = {
        "walking_map_ready":        False,
        "transit_map_ready":        False,
        "frequency_maps_ready":    False,
        # "frequency_map_2_ready":    False,
        # "frequency_map_3_ready":    False,
    }
    for key, value in initial_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


############################# Bus Arrival Rates #############################

@st.cache
def load_needed_tables():
    trips = gtfs.load_prepared_gtfs_table("trips")
    stop_times = gtfs.load_prepared_gtfs_table("stop_times")
    stops = gtfs.load_prepared_gtfs_table("stops")
    return trips, stop_times, stops


def how_often_does_the_bus_come(stop_times, stops):
    # st.markdown("**Bus Arrivals per Hour**")
    st.markdown("##### Bus Arrivals per Hour")
    col1, col2 = st.columns(2)
    
    # The 50 bus
    stop_id = 8920
    bus_arrivals_per_hour(stop_times, stops, stop_id, col1, "The 50 Bus")

    # The 66 bus
    stop_id = 552
    bus_arrivals_per_hour(stop_times, stops, stop_id, col2, "The 66 Bus")


def bus_arrivals_per_hour(stop_times, stops, stop_id, st_col, ttl):
    chart_df = bus_stop_histogram(stop_times, stop_id)
    layer_spec = bus_stop_histogram_layer_spec(stops, stop_id, ttl)
    
    spec = {
        # "title":    "Chart Main Title",
        "layer":    layer_spec,
    }
    st_col.vega_lite_chart(data=chart_df, spec=spec, use_container_width=True)


def bus_stop_histogram(stop_times, stop_id):
    # Chart Data
    chart_df = stop_times[stop_times["stop_id"] == stop_id]
    chart_df = chart_df["hour_of_arrival"].value_counts().sort_index()
    chart_df = pd.DataFrame(chart_df).reset_index()
    chart_df.rename(columns={
        "index": "Hour of Arrival",
        "hour_of_arrival": "Buses Per Hour"},
        inplace=True)
    return chart_df


def bus_stop_histogram_layer_spec(stops, stop_id, ttl):
    stop_desc = stops[stops["stop_id"] == stop_id]["stop_desc"].iloc[0]
    stop_name = stop_desc.split(",")[0].strip()
    direction = stop_desc.split(",")[1].strip()

    histogram_spec = {
        "mark": "bar",
        "title": [ttl, f"{direction} from {stop_name}"],
        "encoding": {
            "x": {
                "field": "Hour of Arrival", 
                "type": "ordinal",
                "axis": {"labelAngle": 0},
            },
            "y": {
                "field": "Buses Per Hour",
                "type": "quantitative",
                "title": "No. Buses per Hour, Average",
            },
        }
    }
    rule_spec = {
        "mark": "rule",
        "encoding": {
            "y": {
                "field": "Buses Per Hour",
                "aggregate":    "mean",
                },
            "size": {"value": 2},
        }
    }
    layer_spec = [histogram_spec, rule_spec]
    return layer_spec


######################## Wait Time Simulation ########################

def generate_bus_and_people_times(bus_frequency, num_days=7, people_per_day=1000):
    """
    Originally, I generated bus times by sampling from a poisson distribution 
    and adding those wait times up consecutively to get the bus arrival times. 
    This produced bus times that averaged to the right frequency, but the 
    average wait times for people came to half the bus frequency. I was 
    perplexed, and still don't quite understand why, but plenty of research has 
    confirmed that the probabalistically correct wait times should equal the 
    bus arrival rate, and that sampling bus arrival times randomly from a 
    uniform distribution gets the same distribution as sampling from a poisson 
    distribution.
    """
    time_length = num_days * 24 * 60 #one week
    num_buses = time_length // bus_frequency
    num_people = people_per_day * num_days

    # It was not what I first expected
    bus_times = num_buses * bus_frequency * random.random(num_buses)
    people_times = bus_times.max() * random.random(num_people)
    bus_times = np.sort(bus_times)
    people_times = np.sort(people_times)
    return bus_times, people_times


def plot_simulated_arrival_times(bus_arrivals, people_arrivals):
    # Let's zoom in to two hours, between
    ten_am = 60 * 10
    one_pm = 60 * 12
    bus_arrivals = bus_arrivals[(bus_arrivals > ten_am) & (bus_arrivals < one_pm)]
    people_arrivals = people_arrivals[(people_arrivals > ten_am) & (people_arrivals < one_pm)]

    format_timestamp = lambda mins: f"5 Sep 2022 {int(mins//60)}:{int(mins%60)}:00"
    times = []
    category = []
    for time in bus_arrivals:
        times.append(format_timestamp(time))
        category.append("Bus Arrival")

    for time in people_arrivals:
        times.append(format_timestamp(time))
        category.append("People Arrivals")
    
    df = pd.DataFrame()
    df["Arrivals"] = times
    df["Category"] = category

    histogram_spec = {
        "mark": "bar",
        "transform": [{"filter": "datum.Category == 'People Arrivals'"}],
        "format": {
            "parse": {"Arrivals": "utc:'%d %b %Y %H:%M:%S'"}
            },
        "encoding": {
            "x": {
                "timeUnit": {
                    "unit": "hoursminutes",
                    "step": 2,
                },
                "field":    "Arrivals", 
                "title": "Time",
                "axis": {"tickCount": 10},
            },
            "y": {
                "aggregate": "count",
                "title": ["No. People Arriving", "at the Bus Stop"],
                "axis": {"tickMinStep": 1},
            },
            "color": {
                "field": "Category", 
                "type": "nominal", 
                "scale": {"range": ["#31333f", "#1f77b4"]},
            },
        }
    }
    rule_spec = {
        "mark": "rule",
        "transform": [{"filter": "datum.Category == 'Bus Arrival'"}],
        "encoding": {
            "x": {
                "timeUnit": "hoursminutes",
                "field": "Arrivals", 
            },
            "size": {"value": 2},
            "color": {
                "field": "Category", 
                "type": "nominal", 
                "scale": {"range": ["#31333f", "#1f77b4"]},
            },
        }
    }
    spec = {
        "title": "Two Hours of Simulated People Waiting for a Simulated Bus",
        "height": 200,
        "layer": [histogram_spec, rule_spec]
    }
    st.vega_lite_chart(data=df, spec=spec, use_container_width=True)


def bus_time_metrics(bus_times, people_times):
    avg_btwn_time = np.mean(np.diff(bus_times))
    avg_wait_time = average_wait_time(bus_times, people_times)

    col1, col2 = st.columns(2)
    col1.metric("Average Time Between Buses", f"{round(avg_btwn_time, 1)} min")
    col2.metric("Avg. Passenger Wait", f"{round(avg_wait_time, 1)} min")


def average_wait_time(bus_times, people_times):
    ii = np.searchsorted(bus_times, people_times, side="right")
    wait_times = bus_times[ii] - people_times
    return wait_times.mean()


############################## Geocode Check ##############################

def address_can_be_found(address):
    """Ensure that if the address cannot be found the site fails gracefully"""
    try:
        _ = ox.geocoder.geocode(address)
        return True
    except ValueError:
        # Nominatim could not geocode the query
        return False


def display_dora():
    buffer = 0.25
    _, col1, _, col2, _ = st.columns([buffer, 2, buffer, 5, buffer])
    # col1.write("")
    col1.image("img/dora_and_her_map.webp")
    col2.text("Oh no!")
    col2.text("""
        I'm sorry. I couldn't find that location on my 
        map. I got it for free from some nice people on 
        the internet, but sometimes it's missing things!
        Please try another address.
        """)


def geocode_check(make_isochrone_func):
    def wrapper(*args):
        address = args[0]
        if address_can_be_found(address):
            return make_isochrone_func(*args)
        else:
            display_dora()
    return wrapper


############################### Walking Map ###############################

def walking_address_input():
    col1, col2 = st.columns([7,2])

    # label = """
    #     Enter an address below to generate a map of everywhere you can walk 
    #     from that spot.
    # """
    label = "Enter an address below to generate a map of everywhere you can walk from that spot."
    address = col1.text_input(label, key="address", 
        placeholder="Enter your Address")

    col2.write("")
    col2.write("")
    if address:
        street_address = address.split(",")[0]
    else:
        street_address = None
    walking_isochrone_download_button(col2, street_address)
    return address


@geocode_check
@st.experimental_memo()
def make_walking_isochrone(address):
    """
    TKTK
    """
    st.session_state["walking_map_ready"] = False
    
    city = "Chicago, Illinois"
    chicago = graphs.load_citywide_graph(city)
    in_chicago, lat_lng = address_is_in_chicago(address, chicago)

    if in_chicago:
        graph = chicago
    else:
        graph, lat_lng = graphs.download_graph_from_address(address)

    filepath = "plots/user_generated_walking_isochrone.png"
    walking_isochrone = WalkingIsochrone(citywide_graph=graph)
    _ = walking_isochrone.make_isochrone(lat_lng, filepath=filepath)
    st.session_state["walking_map_ready"] = True



def address_is_in_chicago(address, chicago):
    lat_lon = ox.geocoder.geocode(address)
    # lat_lon = geocode_gracefully(address)
    # if lat_lon is not None:
    lat, lon = lat_lon[0], lat_lon[1]
    nearest_node = ox.distance.nearest_nodes(chicago, lon, lat)
    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]
    node_lat = chicago.nodes[nearest_node]["y"]
    node_lon = chicago.nodes[nearest_node]["x"]

    threshold = 0.0008
    if abs(node_lat-lat) < threshold and abs(node_lon-lon) < threshold:
        return True, (node_lat, node_lon)
    else:
        return False, None


def walking_isochrone_download_button(st_col, street_address):
    filepath = "plots/user_generated_walking_isochrone.png" 
    with open(filepath, "rb") as image_file:
        st_col.download_button("Download Map", 
            data=image_file,
            file_name=f"{street_address}.png",
            mime="image/png",
            disabled=not st.session_state["walking_map_ready"])

############################### Transit Map ###############################


def transit_address_input():
    # col1, col2, col3 = st.columns([7,2,3])
    col1, col2 = st.columns([7,2])

    # label = """
    #     Enter an address below to generate a map of everywhere transit can take 
    #     you from that spot.
    # """
    label = "Enter an address below to generate a map of everywhere transit can take you from that spot. This may take a few minutes."
    address = col1.text_input(label, key="transit_address",
        placeholder="Enter your Address")

    col2.write("")
    col2.write("")
    transit_isochrone_download_button(col2, address)
    return address


@geocode_check
@st.experimental_memo
def make_transit_isochrone(address):
    st.session_state["transit_map_ready"] = False
    transit_isochrone = TransitIsochrone(DATA_DIR, "Chicago, Illinois")
    lat_lon = ox.geocoder.geocode(address)

    # trip_times = [15, 30, 45, 60]
    trip_times = [15, 30, 45]
    freq_multipliers = [1]
    filepath = "plots/user_generated_transit_isochrone.png"
    transit_isochrone.make_isochrone(lat_lon, 
        trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        cmap="plasma")
    st.session_state["transit_map_ready"] = True


def transit_isochrone_download_button(st_col, address):
    if address:
        street_address = address.split(",")[0]
    else:
        street_address = None

    filepath = "plots/user_generated_transit_isochrone.png" 
    with open(filepath, "rb") as image_file:
        st_col.download_button("Download Map", 
            data=image_file,
            file_name=f"{street_address}.png",
            mime="image/png",
            disabled=not st.session_state["transit_map_ready"],
            key="transit_download")


############################## Frequency Maps ##############################

def thirty_minute_maps():
    st.write("")
    st.markdown("###### Thirty Minute Trips at Increasing Rates of Service")
    col1, col2, col3 = st.columns(3)

    with col1:
        filename = "plots/thirty_minute_reduced_service.png"
        caption  = "Half Scheduled Service"
        st.image(filename, caption=caption)

    with col2:
        filename = "plots/thirty_minute_scheduled_service.png"
        caption  = "Scheduled Service"
        st.image(filename, caption=caption)

    with col3:
        filename = "plots/thirty_minute_enhanced_service.png"
        caption  = "Twice Scheduled Service"
        st.image(filename, caption=caption)


def forty_five_and_one_hour_maps():
    caption = """
        Coverage area for service at half of what is scheduled, as scheduled, 
        twice as often as scheduled, and three times.
        """
    st.write("")
    st.markdown("###### Forty Five Minute Trips at Increasing Rates of Service")
    frequency_isochrone = "plots/frequency_isochrone_45_min_trips.png"
    st.image(frequency_isochrone, caption=caption)

    st.write("")
    st.markdown("###### One Hour Trips at Increasing Rates of Service")
    frequency_isochrone = "plots/frequency_isochrone_60_min_trips.png"
    st.image(frequency_isochrone, caption=caption)


def frequency_address_input():
    col1, col2 = st.columns([7,2])

    label = """
        Enter an address below to generate maps of transit with better and 
        better schedules.
    """
    address = col1.text_input(label, key="frequency_address",
        placeholder="Enter your Address")

    col2.write("")
    col2.write("")
    frequency_isochrone_download_button(col2, address)
    return address


@geocode_check
@st.experimental_memo
def make_frequency_isochrones(address):
    st.session_state["frequency_maps_ready"] = False

    lat_lon = ox.geocoder.geocode(address)
    trip_times = [30]

    freq_multipliers = [2]
    filepath = FREQUENCY_DIR / "enhanced_service.png"
    transit_isochrone = TransitIsochrone(DATA_DIR, "Chicago, Illinois")
    bbox = transit_isochrone.make_isochrone(lat_lon, 
        trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        color="#4767AF")

    freq_multipliers = [1]
    filepath = FREQUENCY_DIR / "scheduled_service.png"
    transit_isochrone = TransitIsochrone(DATA_DIR, "Chicago, Illinois")
    _ = transit_isochrone.make_isochrone(lat_lon, 
        trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        color="#9EACCB",
        bbox=bbox)

    freq_multipliers = [0.5]
    filepath = FREQUENCY_DIR / "reduced_service.png"
    transit_isochrone = TransitIsochrone(DATA_DIR, "Chicago, Illinois")
    _ = transit_isochrone.make_isochrone(lat_lon, 
        trip_times=trip_times, 
        freq_multipliers=freq_multipliers,
        filepath=filepath,
        color="#7C94CB",
        bbox=bbox)
    st.session_state["frequency_maps_ready"] = True


def frequency_isochrone_download_button(st_col, address):
    if address:
        street_address = address.split(",")[0]
    else:
        street_address = None

    # deliberately using strings and not the Path objects
    filenames = [
        "user_generated_frequency_maps/enhanced_service.png",
        "user_generated_frequency_maps/scheduled_service.png",
        "user_generated_frequency_maps/reduced_service.png"
    ]

    zip_filename = "frequency_maps.zip"
    zipObj = ZipFile(zip_filename, "w")
    if st.session_state["frequency_maps_ready"]:
        for filepath in filenames:
            zipObj.write(filepath)
    zipObj.close()

    with open(zip_filename, "rb") as zip_file:
        st_col.download_button("Download Maps", 
            data=zip_file,
            file_name=f"{street_address}.zip",
            disabled=not st.session_state["frequency_maps_ready"],
            key="frequency_maps_download")


def user_generated_thirty_minute_maps():
    col1, col2, col3 = st.columns(3)

    filename = FREQUENCY_DIR / "enhanced_service.png"
    caption  = "Twice Scheduled Service"
    col3.image(str(filename), caption=caption)

    filename = FREQUENCY_DIR / "scheduled_service.png"
    caption  = "Scheduled Service"
    col2.image(str(filename), caption=caption)

    filename = FREQUENCY_DIR / "reduced_service.png"
    caption  = "Half Scheduled Service"
    col1.image(str(filename), caption=caption)

