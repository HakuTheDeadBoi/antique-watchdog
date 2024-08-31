import threading
import yaml

from aw import QUERIES_YAML_FILE
from aw.constraint import Constraint
from aw.error import QueriesNotLoadedError, CloseThreadError
from aw.query import Query

class QueryManager:
    def __init__(self):
        self._queries_file_lock = threading.Lock()

    def _load_queries_from_file(self) -> list[dict]:
        try:
            with open(QUERIES_YAML_FILE, "r") as file:
                data = yaml.safe_load(file)
                return data or []
        except FileNotFoundError as e:
            raise QueriesNotLoadedError("Queries cannot be loaded.")
        
    def _create_new_file(self) -> None:
        try:
            with open(QUERIES_YAML_FILE, "r") as file:
                pass
        except IOError:
            raise CloseThreadError("Cannot create queries file.")
        
    def _save_queries_to_file(self, queries: list[dict]) -> None:
        try:
            with open(QUERIES_YAML_FILE, "w") as file:
                yaml.dump(queries, file)
        except IOError:
            raise IOError("Error dumping queries.")

    def _constraint_to_dict(self, constraint: Constraint) -> dict:
        return {
            "id": constraint.id,
            "key": constraint.key,
            "value": constraint.value,
            "relation": constraint.relation,
            "asciize": constraint.asciize
        }

    def _query_to_dict(self, query: Query) -> dict:
        return {
            "id": query.id,
            "query_string": query.query_string,
            "asciize": query.asciize,
            "constraint_list": [self._constraint_to_dict(con) for con in query.constraint_list]
        }
    
    def _to_query(self, query_dict: dict) -> Query:
        return Query(
            id = query_dict["id"],
            query_string = query_dict["query_string"],
            asciize = query_dict["asciize"],
            constraint_list = [self._to_constraint(con) for con in query_dict["constraint_list"]]
        )
    
    def _to_constraint(self, con_dict: dict) -> Constraint:
        return Constraint(
            id = con_dict["id"],
            key = con_dict["key"],
            value = con_dict["value"],
            relation = con_dict["relation"],
            asciize = con_dict["asciize"]
        )

    def fetch_queries(self) -> list[Query]:
        with self._queries_file_lock:
            query_dict_list = self._load_queries_from_file()
            return [self._to_query(query) for query in query_dict_list]
        
    def update_queries(self, queries: list[Query]) -> None:
        with self._queries_file_lock:
            serialized_queries = [self._query_to_dict(query) for query in queries]
            self._save_queries_to_file(serialized_queries)