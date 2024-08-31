class CloseThreadError(Exception):
    """Exception indicating that a thread should be closed without stopping the scheduler."""
    pass

class SkipRecordError(Exception):
    """Exception indicating record wasn't successfully fetched and should not be included."""

class QueriesNotLoadedError(Exception):
    """Exception indicating queries cannot be loaded from file."""