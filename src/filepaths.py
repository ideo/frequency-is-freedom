from pathlib import Path

REPO_ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT_DIR / "data"
GRAPH_PATH = DATA_DIR / "chicago.pkl"
DATAFRAME_PATH = DATA_DIR / "average_travel_times_btwn_stops.csv"
# GTFS_PATH = DATA_DIR / "us-illinois-chicago-transit-authority-cta-gtfs-389/"
GTFS_PATH = DATA_DIR / "gtfs_raw"
