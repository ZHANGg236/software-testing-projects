import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"
DATA_DIR = PROJECT_ROOT / "data"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"

HEADLESS = os.getenv("HEADLESS", "true").lower() not in {"0", "false", "no"}
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH", "")
DEFAULT_TIMEOUT = int(os.getenv("UI_TIMEOUT", "10"))
