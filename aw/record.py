from dataclasses import dataclass

@dataclass
class Record:
    name: str
    author: str
    price: str
    publisher: str
    issue_year: str
    link: str
    language: str = "Není uveden"