# Frequency is Freedom


### Development

1. This project uses [Poetry](https://python-poetry.org/) to manage dependencies. If you don't yet have Poetry, the latest installation instructions can be found [here](https://python-poetry.org/docs/master/#installation). Install all needed packages with:
   ```bash
   poetry install
   ```

1. If you would like to work with jupyter notebooks while using poetry, after running `poetry install`, run:
   ```bash
   poetry run python -m ipykernel install --user --name frequency-is-freedom
   poetry run jupyter lab
   ```
   And then select the newly created kernel, `frequency-is-freedom`.


### To-Do List
- [ ] ~Geocode tool to return the lat/lng of an address within Chicago~
- [ ] Use `osmnx.graph.graph_from_address` to get the starting graph from an address. It can geocode for you, returning a lat/lng
- [ ] Can we download just a graph of a Chicago first, keep that in memory, and use that as a starting point?
- [ ] Use `osmnx.plot.plot_figure_ground` to make very pretty plots like [these](https://i0.wp.com/geoffboeing.com/wp-content/uploads/2017/04/square-mile-street-networks.jpg?ssl=1). 
- [ ] Can I instead color the edges of the graph?
- [ ] Multiple walking speeds
