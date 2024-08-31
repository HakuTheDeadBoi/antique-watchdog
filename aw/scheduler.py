from datetime import datetime
import threading
from time import sleep

from aw import TIME, PERIOD, WEEKDAY
from aw import SLEEP_SCHEDULER_CYCLE_FOR_MINUTE
from aw.config import Config
from aw.querymanager import QueryManager
from aw.tasker import Tasker

class Scheduler:
    def __init__(self, p_config: Config, p_query_manager: QueryManager):
        self.config = p_config
        self.query_manager = p_query_manager
        if self.config.is_valid():
            self.enabled = True
        else:
            self.enabled = False

        self.schedule()

    def _check_time(self) -> bool:
        current_time = datetime.now()

        if self.period == "hourly":
            return current_time.strftime("%M") == self.time[3:]
        if self.period == "daily":
            return current_time.strftime("%H:%M") == self.time
        if self.period == "weekly":
            return current_time.strftime("%H:%M") == self.time and current_time.weekday() == self.day
        
    def schedule(self):
        cf_dict = self.config.get_scheduler_keys()
        self.time = cf_dict[TIME]
        self.day = int(cf_dict[WEEKDAY])
        self.period = cf_dict[PERIOD]

        if self.config.is_valid():
            self.enable()
        else:
            self.disable() 

    def enable(self):
        if self.config.is_valid():
            self.enabled = True
        else:
            pass
            # log unsuccessful attempt to enable scheduler

    def disable(self):
        self.enabled = False

    def start(self):
        while True:
            if not self.enabled:
                continue

            if not self.config.is_scheduler_up_to_date():
                self.schedule()

            if self._check_time():
                try:
                    tasker_thread = threading.Thread(target=Tasker.do_task, args=(self.config, self.query_manager))
                    tasker_thread.setDaemon(True)
                    tasker_thread.start()
                except Exception as e:
                    print("Closed for unknown reason: {e}")

                sleep(SLEEP_SCHEDULER_CYCLE_FOR_MINUTE)
