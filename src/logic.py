from cgi import test
import pandas as pd
import streamlit as st
import numpy as np
from numpy import random
random = random.RandomState(42)

from .text import TEXT


def write_text(section_title, header_level=3):
    # st.subheader(section_title)
    header_hashes = "#"*header_level
    st.markdown(f"{header_hashes} {section_title}")
    for paragraph in TEXT[section_title]:
        st.write(paragraph)


# Simulated Bus Arrival Times
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
    bus_frequency = 15 #minutes
    time_length = num_days * 24 * 60 #one week
    num_buses = time_length // bus_frequency
    num_people = people_per_day * num_days

    # It was not what I first expected
    bus_times = num_buses * bus_frequency * random.random(num_buses)
    people_times = bus_times.max() * random.random(num_people)
    bus_times = np.sort(bus_times)
    people_times = np.sort(people_times)
    return bus_times, people_times


def average_wait_time(bus_times, people_times):
    ii = np.searchsorted(bus_times, people_times, side="right")
    wait_times = bus_times[ii] - people_times
    return wait_times.mean()


def bus_time_metrics(bus_times, people_times):
    avg_btwn_time = np.mean(np.diff(bus_times))
    avg_wait_time = average_wait_time(bus_times, people_times)

    # mins_btwn = int(avg_btwn//1)
    # secs_btwn = int(avg_btwn%60)
    # st.metric("Average Time Between Buses", f"{mins_btwn} min {secs_btwn} sec")
    col1, col2 = st.columns(2)
    col1.metric("Average Time Between Buses", f"{round(avg_btwn_time, 1)} min")
    col2.metric("Avg. Passenger Wait", f"{round(avg_wait_time, 1)} min")


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