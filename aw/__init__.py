from pathlib import Path

# root directory where the whole project is placed
ROOT_DIR = Path(__file__).parent.parent

# config file names relative to ROOT_DIR
CONFIG_FILE = "config.json"
CONFIG_NOTJSON_FILE = "config.notjson"

# config keys, used at various places to read values from config
SERVER_ADDR_KEY = "SERVER_ADDR"
SERVER_PORT_KEY = "SERVER_PORT"
LOGIN_MAIL_KEY = "LOGIN_MAIL"
LOGIN_PASSWORD_KEY = "LOGIN_PASSWORD"
TARGET_MAIL_KEY = "TARGET_MAIL"
SCRAPERS_DIR_KEY = "SCRAPERS_DIR"
