import streamlit as st

import src.logic as lg
from src.text import TEXT
from src.isochrones import generate_isochrone, download_graph_from_address


st.set_page_config(
    page_title="Frequency is Freedom", 
    page_icon="img/usdot_bus_icon.png")

st.markdown("# Frequency is Freedom")


lg.write_text("How Long Do You Wait For The Bus")

lg.write_text("One Day of Simulated Bus Service", header_level=5)
col1, col2 = st.columns(2)
col1.slider("How often does the bus arrive?",
    min_value=1,
    max_value=30,
    value=15,
    key="bus_frequency",
    format="%d minutes")
col2.slider("How many people ride the bus per day?",
    min_value=10,
    max_value=1000,
    value=400,
    key="people_per_day",
    format="%d people",
    step=10)

bus_times, people_times = lg.generate_bus_and_people_times(
    st.session_state["bus_frequency"],
    people_per_day=st.session_state["people_per_day"]
)
lg.plot_simulated_arrival_times(bus_times, people_times)
lg.bus_time_metrics(bus_times, people_times)


# Walking Isochrone
st.text_input("Address", key="address", value="626 W Jackson Blvd, Chicago, IL 60661")
initial_radius = 2.75
graph, lat_lng = download_graph_from_address(st.session_state["address"], 
    radius=initial_radius)


st.subheader("Walking Isochrone")
# my_apartment = (41.897999, -87.675908)
mode = "walk"
   #miles
trip_times = [15, 30, 45, 60]
fig, ttl = generate_isochrone(lat_lng, mode, trip_times, 
    _graph=graph, 
    address=st.session_state["address"])
st.markdown(f"##### {ttl}")
st.pyplot(fig)
lg.isochrone_download_button()


st.markdown("---")
lg.write_text("Citations & Helpful References", header_level=5)