import requests as rq
import re
from bs4 import BeautifulSoup

def main(query):
    search_result = ""
    line_delimiter = '\n'
    item_delimiter = ';'
    url = f"https://trhknih.cz/hledat?q={query}"
    base_url = "https://trhknih.cz"
    response = rq.get(url)

    if response.status_code >= 200 and response.status_code < 300:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        span6_list = soup.find_all("div", attrs={"class": "span6"})

        for span6 in span6_list:
            span_price = span6.find("span", attrs={"class": "ask-count"})
            if span_price:
                record = ""
                link = span6.find("a")["href"]
                book = span6.find("a").text
                price = span6.find("span").text
                year, publisher = span6.find_all("em")[0].text, span6.find_all("em")[1].text

                author = span6.text
                for item in [book, year, publisher, price]:
                    author = author.replace(item, '')
                first_following_escape_idx = author.index('\t')
                author = author[:first_following_escape_idx]
                author = author.strip()

                record = item_delimiter.join((author, book, price, year, publisher, base_url+link))

                search_result += record + line_delimiter
            
        return search_result