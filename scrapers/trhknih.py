import requests as rq
from bs4 import BeautifulSoup
from bs4.element import Tag

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
        full_url = \
            cls.BASE_URL + "/" \
            + cls.ENDPOINT + "?" \
            + cls.Q_PARAM + query_string + "&" \
            + cls.LAST_PARAMS_FULL
        
        return full_url
    
    @classmethod
    def _make_soup(cls, url: str) -> BeautifulSoup:
        response = rq.get(url)
        page_html_content = response.text
        soup = BeautifulSoup(page_html_content, "html.parser")

        return soup
    
    @classmethod
    def _get_serp_item_class_elements(cls, soup: BeautifulSoup) -> list[Tag]:
        return soup.find_all("div", attrs={"class": "serp-item"})

    @classmethod
    def _get_record_from_element(cls, serp_item: Tag) -> "Record":
        span6_div = serp_item.find("div", attrs={"class": "span6"})
        span6_p = span6_div.find("p")
        book_name_a = span6_p.find("a")

        book_name = book_name_a.get_text().strip()

        link = cls.BASE_URL + book_name_a["href"]

        price_span = span6_p.find("span", attrs={"class": "ask-count label label-success"})
        price = price_span.get_text().strip()

        year_em = span6_p.find("em")
        year = year_em.get_text().strip()

        publisher_em = year_em.next_sibling.next_sibling
        publisher = publisher_em.get_text().strip()

        author = year_em.previous_sibling.previous_sibling.strip()

        record = Record(
            name = book_name,
            author = author,
            price = price,
            publisher = publisher,
            issue_year = year,
            link = link
        )

        return record
    
    @classmethod
    def _get_next_page_url(cls, soup: BeautifulSoup) -> str | None:
        paging_navigation_div = soup.find("div", attrs={"class": "pagination pagination-large pagination-left"})

        if paging_navigation_div is None:
            return None

        li_active = paging_navigation_div.find("li", attrs={"class": "active"})
        next_li_to_li_active = li_active.find_next_sibling("li")

        if next_li_to_li_active.get("class") and next_li_to_li_active.get("class")[0] == "disabled":
            return None
        
        a_inside_li = next_li_to_li_active.find("a")

        return cls.BASE_URL + a_inside_li["href"].strip()
        
    @classmethod
    def get_results(cls, query_string: str) -> list[Record]:
        results = []

        url = cls._compose_url(query_string)
        while url is not None:
            soup = cls._make_soup(url)
            serp_item_list = cls._get_serp_item_class_elements(soup)

            for item in serp_item_list:
                record = cls._get_record_from_element(item)
                results.append(record)
        
            url = cls._get_next_page_url(soup)
        
        return results

    








    



        
