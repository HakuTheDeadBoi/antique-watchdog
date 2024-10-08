from datetime import datetime
import threading
from time import sleep

from aw import TIME, PERIOD, WEEKDAY
from aw import SLEEP_SCHEDULER_CYCLE_FOR_MINUTE
from aw.config import Config
from aw.logger import logger
from aw.querymanager import QueryManager
from aw.tasker import Tasker

class Scheduler:
    """
    Manages the scheduling of tasks based on a specified time, period, and configuration.

    Args:
        p_config (Config): Configuration object that includes scheduler settings.
        p_query_manager (QueryManager): Manages queries used in the scheduled tasks.

    Attributes:
        config (Config): Stores the configuration object.
        query_manager (QueryManager): Stores the query manager object.
        enabled (bool): Indicates whether the scheduler is active or not.
        time (str): The time at which tasks should be triggered.
        day (int): The day of the week for weekly tasks (0=Monday, 6=Sunday).
        period (str): The scheduling period ('hourly', 'daily', or 'weekly').

    Methods:
        _check_time() -> bool:
            Checks if the current time matches the scheduled time for the task.
        
        schedule() -> None:
            Loads scheduling details from the configuration and enables or disables the scheduler.
        
        enable() -> None:
            Enables the scheduler if the configuration is valid.
        
        disable() -> None:
            Disables the scheduler.
        
        start() -> None:
            Continuously monitors the time and executes tasks when scheduled.
    """
    def __init__(self, p_config: Config, p_query_manager: QueryManager):
        self.config = p_config
        self.query_manager = p_query_manager
        if self.config.is_valid():
            self.enabled = True
        else:
            self.enabled = False

        self.schedule()

    def _check_time(self) -> bool:
        """
        Checks if the current time matches the scheduled time for the task.

        Returns:
            bool: True if the current time matches the scheduled time, False otherwise.
        """
        current_time = datetime.now()

        if self.period == "hourly":
            return current_time.strftime("%M") == self.time[3:]
        if self.period == "daily":
            return current_time.strftime("%H:%M") == self.time
        if self.period == "weekly":
            return current_time.strftime("%H:%M") == self.time and current_time.weekday() == self.day
        
    def schedule(self):
        """
        Loads scheduling details from the configuration and enables or disables the scheduler.
        """
        cf_dict = self.config.get_scheduler_keys()
        self.time = cf_dict[TIME]
        self.day = int(cf_dict[WEEKDAY])
        self.period = cf_dict[PERIOD]

        if self.config.is_valid():
            self.enable()
        else:
            self.disable() 

    def enable(self):
        """
        Enables the scheduler if the configuration is valid.
        Serves to prevent scheduler from running with invalid configuration
        and also provides external app the way to toggle scheduler in runtime.
        """
        if self.config.is_valid():
            logger.log_success("Scheduler enabled.")
            self.enabled = True
        else:
            logger.log_error("Scheduler enable failed due to invalid configuration.")

    def disable(self):
        """
        Disables the scheduler.
        Also provides external app the way to toggle scheduler in runtime.
        """
        logger.log_success("Scheduler disabled.")
        self.enabled = False

    def start(self):
        """
        Continuously monitors the time and executes tasks when scheduled.
        """
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
                    logger.log_success("Scheduled task started.")
                except Exception as e:
                    logger.log_error(f"Scheduled task halted: {e}")

                sleep(SLEEP_SCHEDULER_CYCLE_FOR_MINUTE)
