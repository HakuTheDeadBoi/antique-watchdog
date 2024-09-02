from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import logging
import os
from os.path import join

from aw import ROOT_DIR, LOG_DIR

class Logger:
    """
    A class to handle logging with time-based rotation for log files.

    This class sets up a logger that writes log messages to a file, rotating the file daily at midnight and keeping up to 60 backup files.

    Attributes:
        _logger (logging.Logger): The logger instance.
        _log_folder (str): The directory where log files are stored.
        _file_handler (TimedRotatingFileHandler): Handler to manage log file rotation.
        _formatter (logging.Formatter): Formatter for log messages.
    """
    def __init__(self):
        """
        Initializes the Logger instance, sets up the logging configuration, and creates the necessary directories if they do not exist.
        
        This method sets the logger to use a TimedRotatingFileHandler with daily rotation at midnight and a backup count of 60. It also sets up the log message format.
        """
        self._logger = logging.getLogger("AWLogger")
        self._logger.setLevel(logging.INFO)
        self._log_folder = join(ROOT_DIR, LOG_DIR)
        try:
            self._file_handler = TimedRotatingFileHandler(join(self._log_folder, datetime.now().strftime("%Y-%m-%d")), when="midnight", interval=1, backupCount=60)
        except FileNotFoundError:
            os.makedirs(join(self._log_folder))
            self._file_handler = TimedRotatingFileHandler(join(self._log_folder, datetime.now().strftime("%Y-%m-%d")), when="midnight", interval=1, backupCount=60)

        self._file_handler.suffix = "%Y%m%d"
        self._formatter = logging.Formatter('%(asctime)s:: %(levelname)s -- %(message)s')
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)
        
    def log_error(self, msg: str) -> None:
        """
        Logs an error message.

        Args:
            msg (str): The error message to be logged.
        
        This method logs the provided message at the ERROR level.
        """
        self._logger.error(msg)

    def log_success(self, msg: str) -> None:
        """
        Logs a success message.

        Args:
            msg (str): The success message to be logged.
        
        This method logs the provided message at the INFO level.
        """
        self._logger.info(msg)

logger = Logger()