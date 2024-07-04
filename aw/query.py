from dataclasses import dataclass

class Query:
    query_string: str
    constraint_list: list["Constraint"] # type: ignore

