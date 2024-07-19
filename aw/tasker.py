from aw.mailer import Mailer
from aw.scrapermanager import ScraperManager

from aw.query import Query
from aw.constraint import Constraint
from aw.util import load_queries

class Tasker:

    @classmethod
    def do_task(cls) -> None:
        queries = load_queries()
        results = ScraperManager.collect_results(queries)
        status = Mailer.send_mail(results)

        print(status, "odesláno")