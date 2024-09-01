import threading

from aw.config import Config
from aw.logger import logger
from aw.querymanager import QueryManager
from aw.scheduler import Scheduler

class AntiqueWatchdog:
    def __init__(self):
        self.config = Config()
        self.querymanager = QueryManager()
        self.scheduler = Scheduler(self.config, self.querymanager)
    
    def run(self):
        try:
            scheduler_thread = threading.Thread(target=self.scheduler.start)
            scheduler_thread.setDaemon(True)
            scheduler_thread.start()
            logger.log_success("Scheduler started")
            return self.scheduler, self.config, self.querymanager
        except Exception as e:
            logger.log_error(e)