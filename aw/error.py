class CloseThreadError(Exception):
    """
    Exception raised when a thread should be closed without stopping the scheduler.

    This exception indicates that a specific thread needs to be terminated, but 
    the scheduler should continue running.
    """

class SkipRecordError(Exception):
    """
    Exception raised when a record was not successfully fetched and should be excluded.

    This exception signifies that a particular record could not be retrieved or 
    processed correctly and therefore should not be included in further operations.
    """

class SkipScraperError(Exception):
    """
    Exception raised when a scraper cannot be used and should be skipped.

    This exception indicates that the scraper in question is not functional or 
    suitable for use in the current context and should be bypassed.
    """

class QueriesNotLoadedError(Exception):
    """
    Exception raised when queries cannot be loaded from a file.

    This exception is used when there is an issue with reading or parsing query 
    definitions from a file, which prevents the queries from being loaded properly.
    """