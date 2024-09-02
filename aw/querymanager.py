import threading
import yaml

from aw import QUERIES_YAML_FILE
from aw.constraint import Constraint
from aw.error import QueriesNotLoadedError, CloseThreadError
from aw.query import Query

class QueryManager:
    """
    Manages the loading, saving, and updating of queries from a YAML file. 

    This class handles synchronization to ensure thread safety when accessing or modifying the queries.

    Attributes:
        _queries_file_lock (threading.Lock): A lock to ensure thread safety when accessing the queries file.
    """
    def __init__(self):
        self._queries_file_lock = threading.Lock()

    def _load_queries_from_file(self) -> list[dict]:
        """
        Loads queries from the YAML file.

        Returns:
            list[dict]: A list of queries loaded from the file. Each query is represented as a dictionary.

        Raises:
            QueriesNotLoadedError: If the queries file cannot be found or loaded.
        """
        try:
            with open(QUERIES_YAML_FILE, "r") as file:
                data = yaml.safe_load(file)
                return data or []
        except FileNotFoundError as e:
            raise QueriesNotLoadedError("Queries cannot be loaded.")
        
    def _create_new_file(self) -> None:
        """
        Creates a new queries file if it doesn't already exist.

        Raises:
            CloseThreadError: If the file cannot be created due to an IOError.
        """
        try:
            with open(QUERIES_YAML_FILE, "r") as file:
                pass
        except IOError:
            raise CloseThreadError("Cannot create queries file.")
        
    def _save_queries_to_file(self, queries: list[dict]) -> None:
        """
        Saves the queries to the YAML file.

        Args:
            queries (list[dict]): A list of queries to save, where each query is represented as a dictionary.

        Raises:
            IOError: If an error occurs during file writing.
        """
        try:
            with open(QUERIES_YAML_FILE, "w") as file:
                yaml.dump(queries, file)
        except IOError:
            raise IOError("Error dumping queries.")

    def _constraint_to_dict(self, constraint: Constraint) -> dict:
        """
        Converts a Constraint object to a dictionary representation.

        Args:
            constraint (Constraint): The constraint to convert.

        Returns:
            dict: The dictionary representation of the constraint.
        """
        return {
            "id": constraint.id,
            "key": constraint.key,
            "value": constraint.value,
            "relation": constraint.relation,
            "asciize": constraint.asciize
        }

    def _query_to_dict(self, query: Query) -> dict:
        """
        Converts a Query object to a dictionary representation.

        Args:
            query (Query): The query to convert.

        Returns:
            dict: The dictionary representation of the query.
        """
        return {
            "id": query.id,
            "query_string": query.query_string,
            "asciize": query.asciize,
            "constraint_list": [self._constraint_to_dict(con) for con in query.constraint_list]
        }
    
    def _to_query(self, query_dict: dict) -> Query:
        """
        Converts a dictionary representation of a query back to a Query object.

        Args:
            query_dict (dict): The dictionary representation of the query.

        Returns:
            Query: The Query object created from the dictionary.
        """
        return Query(
            id = query_dict["id"],
            query_string = query_dict["query_string"],
            asciize = query_dict["asciize"],
            constraint_list = [self._to_constraint(con) for con in query_dict["constraint_list"]]
        )
    
    def _to_constraint(self, con_dict: dict) -> Constraint:
        """
        Converts a dictionary representation of a constraint back to a Constraint object.

        Args:
            con_dict (dict): The dictionary representation of the constraint.

        Returns:
            Constraint: The Constraint object created from the dictionary, or None if the input is empty.
        """
        if con_dict:
            return Constraint(
                id = con_dict["id"],
                key = con_dict["key"],
                value = con_dict["value"],
                relation = con_dict["relation"],
                asciize = con_dict["asciize"]
            )

    def fetch_queries(self) -> list[Query]:
        """
        Fetches and converts all queries from the YAML file into Query objects.

        Returns:
            list[Query]: A list of Query objects loaded from the file.

        Raises:
            QueriesNotLoadedError: If the queries cannot be loaded from the file.
        """
        with self._queries_file_lock:
            query_dict_list = self._load_queries_from_file()
            return [self._to_query(query) for query in query_dict_list]
        
    def update_queries(self, queries: list[Query]) -> None:
        """
        Updates the YAML file with the given list of Query objects.

        Args:
            queries (list[Query]): A list of Query objects to save to the file.

        Raises:
            IOError: If there is an error saving the queries to the file.
        """
        with self._queries_file_lock:
            serialized_queries = [self._query_to_dict(query) for query in queries]
            self._save_queries_to_file(serialized_queries)