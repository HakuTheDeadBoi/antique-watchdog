from pathlib import Path

# root directory where the whole project is placed
ROOT_DIR = Path(__file__).parent.parent

# file names
CONFIG_FILE = "config.ini"
QUERIES_FILE = "queries.json"
QUERIES_YAML_FILE = "queries.yaml"
SCRAPERS_DIR = "scrapers"
LOG_DIR = "logs"

# other stuff
REQUEST_GET_TIMEOUT_LIMIT = 10
CONFIG_SECTION_HEADER = "settings"
SLEEP_SCHEDULER_CYCLE_FOR_MINUTE = 60

# keys
LOGIN = "login"
PASSWORD = "password"
RECIPIENT = "recipient"
SERVER = "server"
PORT = "port"
TIME = "time"
PERIOD = "period"
WEEKDAY = "weekday"

# ConfigEditor
CE_WIDTH = 800
CE_HEIGHT = 800
CE_TITLE = "ConfigEditor"

# day - number map
DAY_TO_INT_MAP = {
    "monday": "0",
    "tuesday": "1",
    "wednesday": "2",
    "thursday": "3",
    "friday": "4",
    "saturday": "5",
    "sunday": "6"
}

# number - day map
INT_TO_DAY_MAP = {
    "0": "monday",
    "1": "tuesday",
    "2": "wednesday",
    "3": "thursday",
    "4": "friday",
    "5": "saturday",
    "6": "sunday",
}