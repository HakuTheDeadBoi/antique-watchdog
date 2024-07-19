from datetime import datetime
import threading
from time import sleep

from aw import SCHED_TIME_KEY, SCHED_PERIOD_KEY, SCHED_WEEKDAY_KEY
from aw.error import CloseThreadError
from aw.tasker import Tasker
from aw.util import config_loader

class Scheduler:
    def __init__(self, p_time: str | None = None, p_day: str | None = None, p_period: str | None = None):
        if not (p_time or p_day or p_period):
            config_dict = config_loader([SCHED_TIME_KEY, SCHED_WEEKDAY_KEY, SCHED_PERIOD_KEY])
            self.time = config_dict[SCHED_TIME_KEY]
            self.day = int(config_dict[SCHED_WEEKDAY_KEY])
            self.period = config_dict[SCHED_PERIOD_KEY]
        else:
            self.time = p_time
            self.day = int(p_day)
            self.period = p_period
        
        self.enabled = True
        self.lock = threading.Lock()

    def _check_time(self) -> bool:
        current_time = datetime.now()

        if self.period == "hourly":
            return current_time.strftime("%M") == self.time[3:]
        if self.period == "daily":
            return current_time.strftime("%H:%M") == self.time
        if self.period == "weekly":
            return current_time.strftime("%H:%M") == self.time and current_time.weekday() == self.day
        
    def reschedule(self, p_time: str | None = None, p_day: str | None = None, p_period: str | None = None):
        if not (p_time, p_day, p_period):
            config_dict = config_loader([SCHED_TIME_KEY, SCHED_WEEKDAY_KEY, SCHED_PERIOD_KEY])
            self.time = config_dict[SCHED_TIME_KEY]
            self.day = int(config_dict[SCHED_WEEKDAY_KEY])
            self.period = config_dict[SCHED_PERIOD_KEY]
        else:
            self.time = p_time
            self.day = int(p_day)
            self.period = p_period

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def start(self):
        while self.enabled:
            with self.lock:
                if self._check_time():
                    try:
                        threading.Thread(target=Tasker.do_task).start()
                    except CloseThreadError:
                        print("Thread closed for known reason.")
                    except Exception as e:
                        print("Closed for unknown reason: {e}")

            sleep(60) # set for one test in one minute
