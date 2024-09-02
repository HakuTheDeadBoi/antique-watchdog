class CloseThreadError(Exception):
    """Exception indicating that a thread should be closed without stopping the scheduler."""
    pass

class SkipRecordError(Exception):
    """Exception indicating record wasn't successfully fetched and should not be included."""

class SkipScraperError(Exception):
    """Exception indicating scraper can't be used and it should be skipped."""

class QueriesNotLoadedError(Exception):
    """Exception indicating queries cannot be loaded from file."""