from aw.mailer import Mailer
from aw.scrapermanager import ScraperManager

from aw.config import Config
from aw.error import CloseThreadError
from aw.querymanager import QueryManager

class Tasker:

    @classmethod
    def do_task(cls, config: Config, qm: QueryManager) -> None:
        try:
            queries = qm.fetch_queries()
            results = ScraperManager.collect_results(queries)
            status = Mailer.send_mail(results, config)
            print(status, "odesláno")
        except CloseThreadError as e:
            print(e)
            # place for logging thread handling