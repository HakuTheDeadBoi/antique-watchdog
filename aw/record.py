from dataclasses import dataclass

@dataclass
class Record:
    name: str
    author: str
    language: str = "Není uveden"
    price: str
    publisher: str
    issue_year: str
    link: str