import importlib
import os
from types import ModuleType
from unidecode import unidecode

from aw import SCRAPERS_DIR

from aw.constraint import Constraint
from aw.error import CloseThreadError
from aw.logger import logger
from aw.query import Query
from aw.record import Record
from aw.scraper import Scraper

class ScraperManager: 
    @classmethod
    def _get_files_from_scrapers_directory(cls, dir_name:str) -> list[str]:
        """
        Get a list of Python file names from the specified directory.

        Args:
            dir_name (str): The directory name where scraper modules are located.

        Returns:
            List[str]: A list of Python file names in the directory.
        """
        try:
            py_files_list = [file for file in os.listdir(dir_name) if file.endswith(".py")]
            return py_files_list
        except IOError as e:
            raise CloseThreadError(f"Error accessing directory '{dir_name}': {e}")
    
    @classmethod
    def _get_modules_from_py_files(cls, py_files: list[str], scrapers_dir: str) -> list[ModuleType]:
        """
        Import modules from a list of Python file names.

        Args:
            py_files (List[str]): A list of Python file names.
            scrapers_dir (str): The directory path where scraper modules are located.

        Returns:
            List[ModuleType]: A list of imported modules.
        """
        modules_list = []

        for py_file in py_files:
            try:
                relative_path = os.path.join(scrapers_dir, py_file)
                spec = importlib.util.spec_from_file_location(os.path.splitext(py_file)[0], relative_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules_list.append(module)
            except (FileNotFoundError, ImportError, AttributeError) as e:
                raise CloseThreadError(f"Error importing module: {e}")

        return modules_list
    
    @classmethod
    def _get_scrapers_from_modules(cls, modules_list: list[ModuleType]) -> list[type[Scraper]]:
        """
        Extract scraper classes from a list of modules.

        Args:
            modules_list (List[ModuleType]): A list of imported modules.

        Returns:
            List[Type[Scraper]]: A list of scraper classes.
        """
        scrapers_list = []

        for module in modules_list:
            for object_name in dir(module): # dir(module) lists all object names in module as strings
                try:
                    object = getattr(module, object_name, None) # try to access attribute by it's name, third arg says return None if nothing found
                    if isinstance(object, type) and issubclass(object, Scraper) and not issubclass(Scraper, object): # exclude Scraper itself, include only subclasses
                        scrapers_list.append(object)
                except AttributeError as e:
                    raise CloseThreadError(f"Error accessing object {object_name} in module {module.__name__}: {e}")

        return scrapers_list
    
    @classmethod
    def _validate_result(cls, record: Record, constraint: Constraint) -> bool:
        """
        Validate a record against a given constraint.

        Args:
            record (Record): The record object to validate.
            constraint (Constraint): The constraint to validate against.

        Returns:
            bool: True if the record passes the constraint, False otherwise.
        """
        try:
            record_value = getattr(record, constraint.key)
            operation = getattr(cls, f"_{constraint.relation}")
            
            final_constraint_value = cls.asciize(constraint.value) if constraint.asciize else constraint.value
            final_record_value = cls.asciize(record_value) if constraint.asciize else record_value

        except AttributeError as e:
            raise CloseThreadError(f"Error trying to get attribute {constraint.key} value from {record}: {e}")
            
        return operation(final_record_value, final_constraint_value)


    @classmethod
    def asciize(cls, text: str) -> str:
        """
        Normalize text to ASCII characters.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
        """
        return unidecode(text).lower()
        
    
    @classmethod
    def _filter_results(cls, constraints: list[Constraint], unfiltered_results: list[Record]) -> list[Record]:
        """
        Filter results based on the constraints.

        Args:
            constraints (List[Constraint]): The list of constraints to apply.
            unfiltered_results (List[Record]): The list of unfiltered result records.

        Returns:
            List[Record]: A list of filtered result records that pass at least one constraint.
        """
        filtered_res = []

        for result in unfiltered_results:
            is_passing = False
            for constraint in constraints:
                if cls._validate_result(result, constraint) == True:
                    is_passing = True
                    break
            
            if is_passing:
                filtered_res.append(result)

        return filtered_res

    @classmethod
    def collect_results(cls, queries: list[Query]) -> list[Record]:
        """
        Collect results for the given queries by executing all scrapers and filtering based on constraints.

        Args:
            queries (List[Query]): A list of queries to execute.

        Returns:
            List[Record]: A list of filtered result records.
        """
        files = cls._get_files_from_scrapers_directory(SCRAPERS_DIR)
        modules = cls._get_modules_from_py_files(files, SCRAPERS_DIR)
        scrapers = cls._get_scrapers_from_modules(modules)
        filtered_results = []

        for query in queries:
            unfiltered_results_per_query = []
            for scraper in scrapers:
                logger.log_success(f"Scraping {scraper.BASE_URL} with query {query.query_string} started.")
                unfiltered_results_per_scraper = scraper.get_results(query.query_string)
                unfiltered_results_per_query.extend(unfiltered_results_per_scraper)
     
            filtered_results.extend(cls._filter_results(query.constraint_list, unfiltered_results_per_query))

        return filtered_results
    
    ##################################
    ###### comparison functions ######
    ##################################

    @classmethod
    def _eq(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is equal to constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is equal to constraint_value, False otherwise.
        """
        return record_value == constraint_value

    @classmethod
    def _nq(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is not equal to constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is not equal to constraint_value, False otherwise.
        """
        return record_value != constraint_value

    @classmethod
    def _gt(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is greater than constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is greater than constraint_value, False otherwise.
        """
        try:
            return int(record_value) > int(constraint_value)
        except ValueError:
            return record_value > constraint_value

    @classmethod
    def _ge(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is greater than or equal to constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is greater than or equal to constraint_value, False otherwise.
        """
        try:
            return int(record_value) >= int(constraint_value)
        except ValueError:
            return record_value >= constraint_value

    @classmethod
    def _lt(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is less than constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is less than constraint_value, False otherwise.
        """
        try:
            return int(record_value) < int(constraint_value)
        except ValueError:
            return record_value < constraint_value

    @classmethod
    def _le(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if record_value is less than or equal to constraint_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if record_value is less than or equal to constraint_value, False otherwise.
        """
        try:
            return int(record_value) <= int(constraint_value)
        except ValueError:
            return record_value <= constraint_value

    @classmethod
    def _in(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if constraint_value is in record_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if constraint_value is in record_value, False otherwise.
        """
        return constraint_value in record_value

    @classmethod
    def _ni(cls, record_value: str, constraint_value: str) -> bool:
        """
        Check if constraint_value is not in record_value.

        Args:
            record_value (str): The value from the record.
            constraint_value (str): The value from the constraint.

        Returns:
            bool: True if constraint_value is not in record_value, False otherwise.
        """
        return constraint_value not in record_value