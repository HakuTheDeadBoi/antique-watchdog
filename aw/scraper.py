from abc import ABC, abstractmethod

class Scraper(ABC):
    """
    An abstract class representing an ideal web scraper.

    This class defines the only one public method
    which is supposed to be an unified interface for scraping manager
    above all scrapers implementing this interface.
    """

    @abstractmethod
    def get_results(self, query_string: str) -> list["Record"]: # type: ignore
        """
        Used to get results from scraping.

        Args:
            query_string (str): Contains query used in URL address.
        
        Returns:
            list[Record]:
                returns a list of Record objects, which are objects containing¨
                every single book record with info about issue, published and link to the shop
            list[]:
                empty list if nothing found
        """
        pass