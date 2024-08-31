from abc import ABC, abstractmethod

class Scraper(ABC):
    """
    Abstract base class for defining a scraper interface.

    Attributes:
        None

    Methods:
        get_results(query_string: str) -> List[Record]:
            Abstract method to retrieve a list of records based on a query string.

            Args:
                query_string (str): The query string to search for.

            Returns:
                List[Record]: A list of Record objects representing the scraped results.
    """
    @abstractmethod
    def get_results(self, query_string: str) -> list["Record"]: # type: ignore
        pass