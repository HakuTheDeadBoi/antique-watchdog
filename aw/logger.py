from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import logging
import os
from os.path import join

from aw import ROOT_DIR, LOG_DIR, LOG_FILE

class Logger:
    def __init__(self):
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
        self._logger.error(msg)

    def log_success(self, msg: str) -> None:
        self._logger.info(msg)

if __name__ == '__main__':
    logger = Logger()
    logger.log_success("HAHA MEME")
    logger.log_error("PRuSR")