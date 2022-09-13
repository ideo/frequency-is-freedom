import streamlit as st

import src.logic as lg
# from src.text import TEXT
# from src.isochrones import generate_walking_isochrone, download_graph_from_address
# import src.isochrones as iso
# from src.plotting import bus_arrivals_per_hour


st.set_page_config(
    page_title="Frequency is Freedom", 
    page_icon="img/usdot_bus_icon.png")
lg.initialize_session_state()


lg.write_text("Frequency is Freedom", header_level=1)
lg.write_text("How Often Does the Bus Come?")
trips, stop_times, stops = lg.load_needed_tables()
lg.how_often_does_the_bus_come(stop_times, stops)
lg.write_text("How Often Does the Bus Come? (II)", header=False)


lg.write_text("How Long Do You Wait For The Bus?")
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


lg.write_text("How Far Can I Go?")
walking_isochrone = "plots/walking_isochrone_from_my_apartment.png"
caption = "How far I can walk from my apartment in 15, 30, 45, and 60 minutes."
st.image(walking_isochrone, caption=caption)
lg.write_text("Geography", header=False)

st.write("")
st.markdown("##### Generate Your Own Walking Map")
address = lg.address_input()
if address:
    lg.make_walking_isochrone(address)


lg.write_text("How Far Can I Go with Public Transit")
transit_isochrone = "plots/transit_isochrone_from_my_apartment.png"
caption = "How far public transit can take me from my apartment in 15, 30, 45, and 60 minutes."
st.image(transit_isochrone, caption=caption)
lg.write_text("How Far Can I Go with Public Transit (II)", header=False)


lg.write_text("More Buses Takes You More Places")
frequency_isochrone = "plots/frequency_isochrone_30_minute_trip.png"
caption = """
    A 30 minute trip from my apartment at 50% reduced service, scheduled 
    service, service 1.5 times as often, and service twice as often.
    """
st.image(frequency_isochrone, caption=caption)

lg.write_text("Better Bus Service")


st.markdown("---")
lg.write_text("Citations & Helpful References", header_level=5)