import requests as rq
from requests import RequestException
from bs4 import BeautifulSoup
from bs4.element import Tag

from aw import REQUEST_GET_TIMEOUT_LIMIT
from aw.error import CloseThreadError, SkipRecordError
from aw.record import Record
from aw.scraper import Scraper

class TrhknihScraper(Scraper):
    """
    A stateless web scraper for extracting data from an URL.

    Attributes:
        BASE_URL (str): base url of the web service
        ENDPOINT (str): search endpoint
        Q_PARAM (str): query parameter without query value
        LAST_PARAMS_FULL: full params following the query
    """

    BASE_URL = "https://www.trhknih.cz"
    ENDPOINT = "hledat" # joined with params 
    Q_PARAM = "q=" # follows endpoint, should be joined with query: ENDPOINT + Q_PARAM
    LAST_PARAMS_FULL = "type=issue&chap=1" # joined to URL: URL&LAST_PARAMS_FULL

    @classmethod
    def _compose_url(cls, query_string: str) -> str:
        """
        Composes the full URL for the search query.

        Args:
            query_string (str): The search query string.

        Returns:
            str: The full URL for the search query.
        """ 
        return f"{cls.BASE_URL}/{cls.ENDPOINT}?{cls.Q_PARAM}{query_string}&{cls.LAST_PARAMS_FULL}"
    
    @classmethod
    def _make_soup(cls, url: str) -> BeautifulSoup:
        """
        Fetches the content of the given URL and parses it into a BeautifulSoup object.

        Args:
            url (str): The URL to fetch.

        Returns:
            BeautifulSoup: The parsed HTML content.

        Raises:
            CloseThreadError: If there is an issue with the network request.
        """
        try:
            response = rq.get(url, timeout=REQUEST_GET_TIMEOUT_LIMIT)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except RequestException as e:
            raise CloseThreadError(f"Failed to fetch {url}: {e}")
    
    @classmethod
    def _get_serp_item_class_elements(cls, soup: BeautifulSoup) -> list[Tag]:
        """
        Extracts the search result items from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            list[Tag]: A list of BeautifulSoup Tag objects representing the search result items.
        """
        return soup.find_all("div", attrs={"class": "serp-item"})

    @classmethod
    def _get_record_from_element(cls, serp_item: Tag) -> "Record":
        """
        Extracts a Record object from a search result item.

        Args:
            serp_item (Tag): The BeautifulSoup Tag object representing the search result item.

        Returns:
            Record: The extracted Record object.

        Raises:
            CloseThreadError: If the expected elements are not found in the search result item.
        """
        try:
            span6_div = serp_item.find("div", attrs={"class": "span6"})
            span6_p = span6_div.find("p") if span6_div else None

            book_name_a = span6_p.find("a") if span6_p else None

            book_name = book_name_a.get_text().strip() if book_name_a else "" 

            link = cls.BASE_URL + book_name_a["href"] if book_name_a else ""

            price_span = span6_p.find("span", attrs={"class": "ask-count label label-success"}) if span6_p else None
            price = price_span.get_text().strip() if price_span else ""

            year_em = span6_p.find("em") if span6_p else None
            year = year_em.get_text().strip() if year_em else ""

            publisher_em = year_em.next_sibling.next_sibling if year_em else None
            publisher = publisher_em.get_text().strip() if publisher_em else ""

            author = year_em.previous_sibling.previous_sibling.strip() if isinstance(year_em.previous_sibling.previous_sibling, str) else ""
        except AttributeError as e:
            raise SkipRecordError(f"Error while trying to scrape book information: {e}")

        return Record(
            name = book_name,
            author = author,
            price = price,
            publisher = publisher,
            issue_year = year,
            link = link
        )
    
    @classmethod
    def _get_next_page_url(cls, soup: BeautifulSoup) -> str | None:
        """
        Extracts the URL of the next page of search results, if available.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            str | None: The URL of the next page of search results, or None if there is no next page.
        """
        pagination_div = soup.find("div", attrs={"class": "pagination pagination-large pagination-left"})

        if pagination_div is None:
            return None

        current_page = pagination_div.find("li", attrs={"class": "active"})
        next_page_li = current_page.find_next_sibling("li")

        if not next_page_li or next_page_li.get("class") == ["disabled"]:
            return None

        next_page_a = next_page_li.find("a")
        return f"{cls.BASE_URL}{next_page_a['href'].strip()}" if next_page_a else None
        
    @classmethod
    def get_results(cls, query_string: str) -> list[Record]:
        """
        Retrieves the search results for the given query string.

        This method iteratively fetches search results from all available pages,
        parses them, and returns a list of Record objects.

        Args:
            query_string (str): The search query string.

        Returns:
            list[Record]: A list of Record objects representing the search results.
            
        Raises:
            CloseThreadError: If network requests fail.
        """
        results = []
        url = cls._compose_url(query_string)

        while url is not None:
            soup = cls._make_soup(url)
            serp_items = cls._get_serp_item_class_elements(soup)

            for item in serp_items:
                try:
                    record = cls._get_record_from_element(item)
                    results.append(record)
                except SkipRecordError as e:
                    # log skipping record
                    pass

            url = cls._get_next_page_url(soup)
        
        return results
    
if __name__ == '__main__':
    try:
        egan_res = TrhknihScraper.get_results("greg egan")
        print("egan should give results: ", egan_res != [])
        dfjodsfjklfsdklsfdjfkld_res = TrhknihScraper.get_results("dfjodsfjklfsdklsfdjfkld")
        print("dfjodsfjklfsdklsfdjfkld should give zero results", dfjodsfjklfsdklsfdjfkld_res == [])
    except CloseThreadError as e:
        print(f"running offline should throw this error: {e}")