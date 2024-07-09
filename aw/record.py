from dataclasses import dataclass

@dataclass
class Record:
    """
    Represents a record containing information about a book or publication.

    Attributes:
        name (str): The name or title of the book.
        author (str): The author(s) of the book.
        price (str): The price of the book.
        publisher (str): The publisher of the book.
        issue_year (str): The year of publication.
        link (str): A link to more information about the book.
        language (str, optional): The language of the book (default is "Neuvedeno").
    """
    name: str
    author: str
    price: str
    publisher: str
    issue_year: str
    link: str
    language: str = "Neuvedeno"