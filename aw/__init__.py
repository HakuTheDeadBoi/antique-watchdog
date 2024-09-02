from pathlib import Path

# root directory where the whole project is placed
ROOT_DIR = Path(__file__).parent.parent
"""
The root directory of the project, defined as the parent directory of the current file's parent.
"""

# file names
CONFIG_FILE = "config.ini"
"""
The name of the configuration file.
"""

QUERIES_FILE = "queries.json"
"""
The name of the JSON file used for storing queries.
"""

QUERIES_YAML_FILE = "queries.yaml"
"""
The name of the YAML file used for storing queries.
"""

SCRAPERS_DIR = "scrapers"
"""
The directory where scraper scripts are stored.
"""

LOG_DIR = "logs"
"""
The directory where log files are stored.
"""

# other stuff
REQUEST_GET_TIMEOUT_LIMIT = 10
"""
The timeout limit (in seconds) for GET requests.
"""

CONFIG_SECTION_HEADER = "settings"
"""
The header name for the configuration section in the config file.
"""

SLEEP_SCHEDULER_CYCLE_FOR_MINUTE = 60
"""
The number of seconds for one cycle of the scheduler.
"""

# keys
LOGIN = "login"
"""
The key used to store and retrieve the login information in the config.
"""

PASSWORD = "password"
"""
The key used to store and retrieve the password information in the config.
"""

RECIPIENT = "recipient"
"""
The key used to store and retrieve the recipient's information in the config.
"""

SERVER = "server"
"""
The key used to store and retrieve the server address in the config.
"""

PORT = "port"
"""
The key used to store and retrieve the port number in the config.
"""

TIME = "time"
"""
The key used to store and retrieve the time setting in the config.
"""

PERIOD = "period"
"""
The key used to store and retrieve the period setting in the config.
"""

WEEKDAY = "weekday"
"""
The key used to store and retrieve the weekday setting in the config.
"""

# ConfigEditor
CE_WIDTH = 800
"""
The width of the ConfigEditor window in pixels.
"""

CE_HEIGHT = 800
"""
The height of the ConfigEditor window in pixels.
"""

CE_TITLE = "ConfigEditor"
"""
The title of the ConfigEditor window.
"""

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
"""
A mapping of day names to their corresponding integer values.
"""

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
"""
A mapping of integer values to their corresponding day names.
"""