# Frequency is Freedom

This project draws maps to show that more frequent transit service, especially especially bus service, gives people more access to their city. The interactive article can be found [here](https://ideo-frequency-is-freedom-app-q4autp.streamlitapp.com/). While the motivation for the project and the focus of the article is my experience in Chicago, the code has been set up so that it could be recreated for any city. It relies upon [OSMNX](https://geoffboeing.com/2016/11/osmnx-python-street-networks/), which is a mash up of Open Street Maps and [NetworkX](https://networkx.org/), and publicly available [GTFS](https://database.mobilitydata.org/) data. If you would like to recreate this project for your city, follow the steps below.

### How this Works

OSMNX allows you to download a NetworkX graph of all walking routes in a city. You can also set a travel time for each edge, taken from a constant walking speed. From the GTFS data we can infer travel times between transit stops, as well as the average time someone would spend waiting for a bus or train at a transit stop. We can then add new edges to the graph, directly connecting transit stops. The travel times for the edges are taken from the sum of how long someone would be stuck waiting, on average, for the bus or train plus the average travel time once riding.

The purpose of this project is to test the effect on the frequency of service, and so the transit travel times are updated each time an isochrone is built so that the wait times reflect the frequency being tested. The isochrone modules can be found in `src/isochrones.py`. See instructions below for generating your own maps


### Development

1. This project uses [Poetry](https://python-poetry.org/) to manage dependencies. If you don't yet have Poetry, the latest installation instructions can be found [here](https://python-poetry.org/docs/master/#installation). Install all needed packages with:
   ```bash
   poetry install
   ```

1. You can find GTFS data from any transit agency that makes it available in [The Mobility Database](https://database.mobilitydata.org/). Once you've found and downloaded your data, add you raw GTFS tables to `data/gtfs_raw` and update the `GTFS_PATH` in `src/filepaths.py` accordingly with whatever subdirectories you may use.. For example, it's been set here to `GTFS_PATH = DATA_DIR / "gtfs_raw/chicago"`

1. To download the citywide network graph and then add transit travel times, update `create_transit_graph.py` with the name of your city. For example, you'll see that within the `if __name__ == "__main__":` loop it's currently set to `city="Chicago, Illinois"`. The city name must be consistent throughout your code, because the city name determines the name of the pickle file where the graph is saved.

1. You may then build the transit graph with: 
   ```bash
   poetry run python create_transit_graph.py
   ```

   The script will prompt you to specify which date you want to pull schedules for. You can also specify a date from the command line. For example, for this article, I specified Monday, August 15th with:
   ```bash
   poetry run python create_transit_graph.py -m 20220815
   ```

1. After creating the graph, you are ready to make some isochrones! A walking isochrone can me made like so:

   ```python
   import osmnx as ox

   from src.filepaths import DATA_DIR
   from src.isochrones import WalkingIsochrone

   address = "626 W Jackson Blvd, Chicago IL"
   lat_lng = ox.geocoder.geocode(address)

   city = "Chicago, Illinois"
   graph = graphs.load_citywide_graph(city)
   walking_isochrone = WalkingIsochrone(graph)

   filepath = "plots/walking_isochrone.png"
   walking_isochrone.make_isochrone(lat_lng, filepath=filepath)
   ```

   And a transit isochrone can be made like so:

   ```python
   import osmnx as ox

   from src.filepaths import DATA_DIR
   from src.isochrones import TransitIsochrone

   address = "626 W Jackson Blvd, Chicago IL"
   lat_lng = ox.geocoder.geocode(address)

   city = "Chicago, Illinois"
   transit_isochrone = TransitIsochrone(DATA_DIR, city)

   trip_times = [15, 30, 45, 60]
   freq_multipliers = [1]
   filepath = "plots/transit_isochrone_from_my_apartment.png"
   transit_isochrone.make_isochrone(my_lat_lon, 
      trip_times=trip_times, 
      freq_multipliers=freq_multipliers,
      filepath=filepath)
   ```

1. To recreate the charts from the article, run:
   ```bash
   poetry run python create_maps_for_article.py
   ```

   You can edit that file to change the starting location and city name. Use the same city name as above, because the city name determines the name of the pickle file where the graph is saved.

1. Optionally, if you would like to work with jupyter notebooks while using poetry, after running `poetry install`, run:
   ```bash
   poetry run python -m ipykernel install --user --name frequency-is-freedom
   poetry run jupyter lab
   ```
   And then select the newly created kernel, `frequency-is-freedom`.

### Ideas for follow up projects
- [ ] Calcualte the coverage area of the isochrones and then calculate statistics for what percentage of the city you can access.
- [ ] Use OSMNX's tie to Open Street Maps to count how many of the city's restaruants, office buildings, greenspace, etc. transit makes accessible to you.
- [ ] Bring in census population data to calculate the labor pool that is available to commute to any one location.
- [ ] Bring in real estate data to show that property value is tied to transit accessibility.