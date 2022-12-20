from pathlib import Path

REPO_ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT_DIR / "data"
GTFS_PATH = DATA_DIR / "gtfs_raw/chicago"

FREQUENCY_DIR = REPO_ROOT_DIR / "user_generated_frequency_maps"
FREQUENCY_DIR.mkdir(parents=True, exist_ok=True)