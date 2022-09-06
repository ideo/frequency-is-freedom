import streamlit as st

import src.logic as lg
from src.text import TEXT


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


lg.write_text("Citations & Further Reading", header_level=5)