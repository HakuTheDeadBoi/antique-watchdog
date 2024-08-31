import configparser
import threading
from os.path import join

from aw import ROOT_DIR, CONFIG_FILE, CONFIG_SECTION_HEADER
from aw import LOGIN, PASSWORD, RECIPIENT, SERVER, PORT, TIME, PERIOD, WEEKDAY
from aw.validator import Validator

class Config:
    def __init__(self) -> None:
        self._parser = configparser.ConfigParser()
        self._io_lock = threading.Lock()
        self._filepath = join(ROOT_DIR, CONFIG_FILE)
        self._scheduler_up_to_date = False

        self._load_file()

    def _load_file(self) -> None:
        try:
            self._parser.clear()
            self._parser.read(self._filepath)
        except FileNotFoundError:
            self._create_new_file()
        except IOError as e:
            # log: error loading config file, left empty
            # or raise error
            pass

    def _create_new_file(self) -> None:
        try:
            open(self._filepath, "w")
        except IOError as e:
            raise Exception("Error creating file, halting program.")

    def _save_file(self) -> None:
        try:
            with open(self._filepath, "w") as file:
                self._parser.write(file)
                file.close()
        except IOError as e:
            raise Exception("Error writing to file, halting program.")
        
    def is_valid(self) -> bool:
        is_valid = True

        is_valid = Validator.validate_email(self._parser[CONFIG_SECTION_HEADER]["login"])
        is_valid = Validator.validate_email(self._parser[CONFIG_SECTION_HEADER]["recipient"])
        is_valid = Validator.validate_server(self._parser[CONFIG_SECTION_HEADER]["server"])
        is_valid = Validator.validate_port(self._parser[CONFIG_SECTION_HEADER]["port"])
        is_valid = Validator.validate_time(self._parser[CONFIG_SECTION_HEADER]["time"])

        return is_valid
    
    def _get_key(self, key: str) -> str:
        try:
            return self._parser[CONFIG_SECTION_HEADER][key]
        except KeyError:
            raise KeyError(f"Key {key} missing.")
    
    def get_key(self, key: str) -> str:
        with self._io_lock:
            return self._get_key(key)
        
    def get_mailer_keys(self) -> dict[str, str]:
        with self._io_lock:
            return {
                LOGIN: self._get_key(LOGIN),
                PASSWORD: self._get_key(PASSWORD),
                RECIPIENT: self._get_key(RECIPIENT),
                SERVER: self._get_key(SERVER),
                PORT: self._get_key(PORT)
            }
        
    def get_scheduler_keys(self) -> dict[str, str]:
        with self._io_lock:
            self._scheduler_up_to_date = True

            return {
                TIME: self._get_key(TIME),
                PERIOD: self._get_key(PERIOD),
                WEEKDAY: self._get_key(WEEKDAY)
            }
    
    def _set_key(self, key: str, value: str) -> None:
        try:
            if key in (TIME, PERIOD, WEEKDAY):
                self._scheduler_up_to_date = False
            self._parser[CONFIG_SECTION_HEADER][key] = value
        except KeyError as e:
            raise Exception("Unable to edit a key, halting program.")
        
    def set_key(self, key: str, value: str) -> None:
        with self._io_lock:
            self._set_key(key, value)
            self._save_file()
    
    def set_multiple_keys(self, key_value_pairs: dict[str, str]) -> None:
        with self._io_lock:
            for key, value in key_value_pairs.items():
                self._set_key(key, value)
            self._save_file()

    def is_scheduler_up_to_date(self) -> bool:
        with self._io_lock:
            return self._scheduler_up_to_date