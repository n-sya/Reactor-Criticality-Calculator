from pathlib import Path


BARN_TO_SQUARE_METRE = 1e-28
CRITICALITY_TOLERANCE = 1e-6

PROJECT_ROOT = Path(__file__).parent
NUCLEAR_DATA_PATH = PROJECT_ROOT / "data" / "nuclear_data.json"

WINDOW_TITLE = "Reactor Criticality Calculator"
WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 760