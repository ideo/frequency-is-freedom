import streamlit as st

import src.logic as lg


st.set_page_config(
    page_title="Frequency is Freedom", 
    # page_icon="img/usdot_bus_icon.png",
    page_icon="oncoming_bus",
    )
lg.initialize_session_state()


st.markdown("# Frequency is Freedom")
st.caption("September, 2022 – words and code by Joe Gambino")
lg.write_text("Frequency is Freedom", header=False)
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

st.markdown("##### Generate Your Own Walking Map")
address = lg.walking_address_input()
if address:
    lg.make_walking_isochrone(address)
    if st.session_state["walking_map_ready"]:
        street_address = address.split(",")[0]
        caption = f"Everywhere someone can walk in 15, 30, 45, and 60 minutes from {street_address}."
        filepath = "plots/user_generated_walking_isochrone.png"
        st.image(filepath, caption=caption)


lg.write_text("How Far Can I Go with Public Transit?")
transit_isochrone = "plots/transit_isochrone_from_my_apartment.png"
caption = "How far public transit can take me from my apartment in 15, 30, 45, and 60 minutes."
st.image(transit_isochrone, caption=caption)

st.markdown("##### Generate Your Own Transit Map")
transit_address = lg.transit_address_input()
if transit_address:
    lg.make_transit_isochrone(transit_address)
    if st.session_state["transit_map_ready"]:
        street_address = transit_address.split(",")[0]
        caption = f"Everywhere someone can take public transit in 15, 30, 45, and 60 minutes from {street_address}."
        filepath = "plots/user_generated_transit_isochrone.png"
        st.image(filepath, caption=caption)


lg.write_text("More Buses Take You More Places")
lg.thirty_minute_maps()
lg.write_text("More Buses Take You More Places (II)", header=False)

caption = """
    Coverage area for service at half of what is scheduled, as scheduled, 
    twice as often as scheduled, and three times.
    """
st.write("")
st.markdown("###### Fourty Five Minute Trips")
frequency_isochrone = "plots/frequency_isochrone_45_min_trips.png"
st.image(frequency_isochrone, caption=caption)

st.write("")
st.markdown("###### One Hour Trips")
frequency_isochrone = "plots/frequency_isochrone_60_min_trips.png"
st.image(frequency_isochrone, caption=caption)

st.markdown("##### Generate Your Own Frequency Maps")
frequency_address = lg.frequency_address_input()
if frequency_address:
    lg.make_frequency_isochrones(frequency_address)
    lg.user_generated_thirty_minute_maps() 


lg.write_text("Better Bus Service")


st.markdown("___")
lg.write_text("Draw Maps For Your City")


st.markdown("---")
lg.write_text("Citations & Helpful References", header_level=5)