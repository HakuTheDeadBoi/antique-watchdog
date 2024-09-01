from aw.mailer import Mailer
from aw.scrapermanager import ScraperManager
from aw.config import Config
from aw.error import CloseThreadError, QueriesNotLoadedError
from aw.logger import logger
from aw.querymanager import QueryManager

class Tasker:
    @classmethod
    def do_task(cls, config: Config, qm: QueryManager) -> None:
        try:
            queries = qm.fetch_queries()
            logger.log_success("Queries fetched successfully.")
            results = ScraperManager.collect_results(queries)
            logger.log_success("Results scraped successfully.")
            status = Mailer.send_mail(results, config)
            if not status:
                logger.log_success("Mail sent successfully.")
            else:
                logger.log_error("Mail sending failed.")
        except CloseThreadError as e:
            logger.log_error(f"Thread unexpectedly closed: {e}")
        except QueriesNotLoadedError:
            logger.log_error("Queries couldn't be loaded. Thread closed.")
        
