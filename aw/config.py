import configparser
import threading
from os.path import join

from aw import ROOT_DIR, CONFIG_FILE, CONFIG_SECTION_HEADER
from aw import LOGIN, PASSWORD, RECIPIENT, SERVER, PORT, TIME, PERIOD, WEEKDAY
from aw.logger import logger
from aw.validator import Validator

class Config:
    """
    A class for managing configuration settings using a configuration file.

    This class handles loading, creating, saving, and validating configuration data
    from and to a file. It provides methods to get and set individual configuration
    values as well as multiple values at once. Thread-safety is ensured using a lock.

    Attributes:
        _parser (configparser.ConfigParser): ConfigParser instance to handle the configuration file.
        _io_lock (threading.Lock): Lock to ensure thread-safe operations on the configuration file.
        _filepath (str): Path to the configuration file.
        _scheduler_up_to_date (bool): Flag indicating if the scheduler configuration is up-to-date.
    """
    def __init__(self) -> None:
        self._parser = configparser.ConfigParser()
        self._io_lock = threading.Lock()
        self._filepath = join(ROOT_DIR, CONFIG_FILE)
        self._scheduler_up_to_date = False

        self._load_file()

    def _load_file(self) -> None:
        """
        Loads the configuration file into the ConfigParser instance.

        If the file does not exist or cannot be read, a new configuration file is created.
        """
        try:
            self._parser.clear()
            result = self._parser.read(self._filepath)
            if not result:
                self._create_new_file()
                self._parser.read(self._filepath)
        except IOError as e:
            logger.log_error("Unable to load config from file.")
            raise IOError from e

    def _create_new_file(self) -> None:
        """
        Creates a new configuration file with a default section header.

        If the file cannot be created, an IOError is raised.
        """
        try:
            with open(self._filepath, "w") as file:
                file.write("[settings]\n")
        except IOError as e:
            logger.log_error("Unable to create a new config file.")
            raise IOError from e

    def _save_file(self) -> None:
        """
        Saves the current configuration to the file.

        Writes the configuration to the file and handles any IOErrors that may occur.
        """
        try:
            with open(self._filepath, "w") as file:
                self._parser.write(file)
                file.close()
        except IOError as e:
            logger.log_error("Unable to save config into file.")
            raise IOError from e
        
    def is_valid(self) -> bool:
        """
        Validates the current configuration settings.

        Returns:
            bool: True if all configuration settings are valid, False otherwise.

        Uses the Validator class to check the validity of email, server, port, and time settings.
        """
        is_valid = True

        is_valid = Validator.validate_email(self._parser[CONFIG_SECTION_HEADER]["login"])
        is_valid = Validator.validate_email(self._parser[CONFIG_SECTION_HEADER]["recipient"])
        is_valid = Validator.validate_server(self._parser[CONFIG_SECTION_HEADER]["server"])
        is_valid = Validator.validate_port(self._parser[CONFIG_SECTION_HEADER]["port"])
        is_valid = Validator.validate_time(self._parser[CONFIG_SECTION_HEADER]["time"])

        return is_valid
    
    def _get_key(self, key: str) -> str:
        """
        Retrieves the value of a specific configuration key.

        Args:
            key (str): The key for which the value is to be retrieved.

        Returns:
            str: The value associated with the given key.

        Raises:
            KeyError: If the key is not found in the configuration file.
        """
        try:
            return self._parser[CONFIG_SECTION_HEADER][key]
        except KeyError as e:
            logger.log_error(f"Unable to get value of config key {key}.")
            raise KeyError from e
    
    def get_key(self, key: str) -> str:
        """
        Thread-safe method to retrieve the value of a configuration key.

        Args:
            key (str): The key for which the value is to be retrieved.

        Returns:
            str: The value associated with the given key.
        """
        with self._io_lock:
            return self._get_key(key)
        
    def get_mailer_keys(self) -> dict[str, str]:
        """
        Retrieves mailer-related configuration settings.

        Returns:
            dict[str, str]: A dictionary containing login, password, recipient, server, and port values.
        """
        with self._io_lock:
            return {
                LOGIN: self._get_key(LOGIN),
                PASSWORD: self._get_key(PASSWORD),
                RECIPIENT: self._get_key(RECIPIENT),
                SERVER: self._get_key(SERVER),
                PORT: self._get_key(PORT)
            }
        
    def get_scheduler_keys(self) -> dict[str, str]:
        """
        Retrieves scheduler-related configuration settings.

        Updates the scheduler status to indicate it is up-to-date and returns
        a dictionary containing time, period, and weekday values.

        Returns:
            dict[str, str]: A dictionary containing time, period, and weekday values.
        """
        with self._io_lock:
            self._scheduler_up_to_date = True

            return {
                TIME: self._get_key(TIME),
                PERIOD: self._get_key(PERIOD),
                WEEKDAY: self._get_key(WEEKDAY)
            }
    
    def _set_key(self, key: str, value: str) -> None:
        """
        Sets the value of a specific configuration key.

        Args:
            key (str): The key to set the value for.
            value (str): The value to set for the key.

        If the key pertains to scheduler settings, the scheduler status is marked as not up-to-date.

        Raises:
            KeyError: If the key is not found in the configuration file.
        """
        try:
            if key in (TIME, PERIOD, WEEKDAY):
                self._scheduler_up_to_date = False
            self._parser[CONFIG_SECTION_HEADER][key] = value
        except KeyError as e:
            logger.log_error(f"Unable to set config key {key} to value {value}")
            raise KeyError from e
        
    def set_key(self, key: str, value: str) -> None:
        """
        Thread-safe method to set the value of a configuration key and save the changes.

        Args:
            key (str): The key to set the value for.
            value (str): The value to set for the key.
        """
        with self._io_lock:
            self._set_key(key, value)
            self._save_file()
    
    def set_multiple_keys(self, key_value_pairs: dict[str, str]) -> None:
        """
        Thread-safe method to set multiple configuration keys and save the changes.

        Args:
            key_value_pairs (dict[str, str]): A dictionary of key-value pairs to be set.
        """
        with self._io_lock:
            for key, value in key_value_pairs.items():
                self._set_key(key, value)
            self._save_file()

    def is_scheduler_up_to_date(self) -> bool:
        """
        Checks if the scheduler configuration is up-to-date.

        Returns:
            bool: True if the scheduler configuration is up-to-date, False otherwise.
        """
        with self._io_lock:
            return self._scheduler_up_to_date