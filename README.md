# Frequency is Freedom

This project draws maps to show that more frequent transit service, especially especially bus service, gives people more access to their city. The interactive article can be found [here](https://ideo-frequency-is-freedom-app-q4autp.streamlitapp.com/). While the motivation for the project and the focus of the article is my experience in Chicago, the code has been set up to work for any city. It relies upon [OSMNX](https://geoffboeing.com/2016/11/osmnx-python-street-networks/), which is a mash up of Open Street Maps and [NetworkX](https://networkx.org/), and publicly available [GTFS](https://database.mobilitydata.org/) data. If you would like to recreate this project for your city, follow the steps below.


### Development

1. This project uses [Poetry](https://python-poetry.org/) to manage dependencies. If you don't yet have Poetry, the latest installation instructions can be found [here](https://python-poetry.org/docs/master/#installation). Install all needed packages with:
   ```bash
   poetry install
   ```

1. Pushed to this repo are all the necessary directories for processing data. You can find GTFS data from any transit agency that makes it available in [The Mobility Database](https://database.mobilitydata.org/). Once you've found and downloaded your data, add you raw GTFS data to `data/gtfs_raw`. 

1. Update `preprocess_data.py` with the name of your city. You can find the current value of `city="Chicago, Illinois"` within the `if __name__ == "__main__":` loop.

1. Run:
   ```bash
   poetry run python preprocess_data.py
   ```  
   This file downloads a citywide network graph and parses the GTFS data to create a transit graph. The isochrone modules rely upon these two graphs to generate maps.

1. Included in `preprocess_data.py` are the functions to generate the maps that appear on the app. You may update these as well to draw maps from your apartment instead of mine, or simply remove the calls to them.

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