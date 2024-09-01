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