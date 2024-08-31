from dataclasses import dataclass

@dataclass
class Query:
    """
    Represents a query with a query string, list of constraints, and optional ASCII normalization.

    Attributes:
        query_string (str): The query string associated with the query.
        constraint_list (List[Constraint]): A list of Constraint objects defining the constraints for the query.
        asciize (bool, optional): If True, normalize string values to ASCII characters (default is True).
    """
    id: int
    query_string: str
    constraint_list: list["Constraint"] # type: ignore
    asciize: bool = True

