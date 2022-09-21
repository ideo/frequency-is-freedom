# Frequency is Freedom

This project explores the effect of frequency of transit schedules on freedom of movement and shows that more frequent service, especially for buses, gives people more access to their city. The interactive article can be found [here](https://ideo-frequency-is-freedom-app-q4autp.streamlitapp.com/). While the motivation for the project and the focus of the article is my experience in Chicago, the code has been set up to work for any city. It relies upon [OSMNX](https://geoffboeing.com/2016/11/osmnx-python-street-networks/), which is a mash up of Open Street Maps and [NetworkX](https://networkx.org/), and publicly available [GTFS](https://database.mobilitydata.org/) data. If you would like to recreate this project for your city, follow the steps below.


### Development

1. This project uses [Poetry](https://python-poetry.org/) to manage dependencies. If you don't yet have Poetry, the latest installation instructions can be found [here](https://python-poetry.org/docs/master/#installation). Install all needed packages with:
   ```bash
   poetry install
   ```



1. All the preprocessed data needed for the app has been pushed to this repo. If you would like to remake this app with newer GTFS data, save your GTFS data to `data/gtfs_raw` and then run:
   ```bash
   poetry run python preprocess_data.py
   ```

1. If you would like to work with jupyter notebooks while using poetry, after running `poetry install`, run:
   ```bash
   poetry run python -m ipykernel install --user --name frequency-is-freedom
   poetry run jupyter lab
   ```
   And then select the newly created kernel, `frequency-is-freedom`.

### Ideas for follow up projects
- [ ] measure coverage area
- [ ] 