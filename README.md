# Frequency is Freedom

This project draws maps to show that more frequent transit service, especially especially bus service, gives people more access to their city. The interactive article can be found [here](https://ideo-frequency-is-freedom-app-q4autp.streamlitapp.com/). While the motivation for the project and the focus of the article is my experience in Chicago, the code has been set up to work for any city. It relies upon [OSMNX](https://geoffboeing.com/2016/11/osmnx-python-street-networks/), which is a mash up of Open Street Maps and [NetworkX](https://networkx.org/), and publicly available [GTFS](https://database.mobilitydata.org/) data. If you would like to recreate this project for your city, follow the steps below.

### How this Works


### Development

1. This project uses [Poetry](https://python-poetry.org/) to manage dependencies. If you don't yet have Poetry, the latest installation instructions can be found [here](https://python-poetry.org/docs/master/#installation). Install all needed packages with:
   ```bash
   poetry install
   ```

1. You can find GTFS data from any transit agency that makes it available in [The Mobility Database](https://database.mobilitydata.org/). Once you've found and downloaded your data, add you raw GTFS tables to `data/gtfs_raw` and update the `GTFS_PATH` in `src/filepaths.py` accordingly with whatever subdirectories you may use.. For example, it's been set here to `GTFS_PATH = DATA_DIR / "gtfs_raw/chicago"`

1. To download the citywide network graph and then add transit travel times, update `create_transit_graph.py` with the name of your city. For example, you'll see that within the `if __name__ == "__main__":` loop it's currently set to `city="Chicago, Illinois"`.

1. You may then build the transit graph with: 
   ```bash
   poetry run python create_transit_graph.py
   ```

   The script will prompt you to specify which date you want to pull schedules for. You can also specify a date from the command line. For example, for this article, I specified Monday, August 15th with 
   ```bash
   poetry run python create_transit_graph.py -m 20220815
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