import threading

from aw.config import Config
from aw.querymanager import QueryManager
from aw.scheduler import Scheduler

class AntiqueWatchdog:
    def __init__(self):
        self.config = Config()
        self.querymanager = QueryManager()
        self.scheduler = Scheduler(self.config, self.querymanager)
    
    def run(self):
        scheduler_thread = threading.Thread(target=self.scheduler.start)
        scheduler_thread.setDaemon(True)
        scheduler_thread.start()
        
        return self.scheduler, self.config, self.querymanager