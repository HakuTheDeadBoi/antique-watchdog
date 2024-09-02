import threading

from aw.config import Config
from aw.logger import logger
from aw.querymanager import QueryManager
from aw.scheduler import Scheduler

class AntiqueWatchdog:
    """
    A class for managing and running the Antique Watchdog application.

    This class initializes configuration, query management, and scheduling components,
    then starts the scheduler in a separate thread. It handles setup and error logging.

    Attributes:
        config (Config): The configuration handler used by the scheduler.
        querymanager (QueryManager): The query manager instance used by the scheduler.
        scheduler (Scheduler): The scheduler instance responsible for scheduling tasks.
    """
    def __init__(self, config: Config|None = None, qm: QueryManager|None = None):
        """
        Initializes the AntiqueWatchdog with optional configuration and query manager instances.

        If no instances are provided, default instances are created. The scheduler is also initialized.

        Args:
            config (Config | None): An optional Config instance. If None, a default Config instance is created.
            qm (QueryManager | None): An optional QueryManager instance. If None, a default QueryManager instance is created.
        """
        self.config = config or Config()
        self.querymanager = qm or QueryManager()
        self.scheduler = Scheduler(self.config, self.querymanager)
    
    def run(self):
        """
        Starts the scheduler in a separate thread and logs its status.

        Creates and starts a daemon thread for the scheduler. Logs a success message if
        the scheduler starts successfully. Logs an error message if an exception occurs.

        Returns:
            tuple: A tuple containing the scheduler, config, and query manager instances.
        """
        try:
            scheduler_thread = threading.Thread(target=self.scheduler.start)
            scheduler_thread.setDaemon(True)
            scheduler_thread.start()
            logger.log_success("Scheduler started")
            return self.scheduler, self.config, self.querymanager
        except Exception as e:
            logger.log_error(e)