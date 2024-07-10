class CloseThreadError(Exception):
    """Exception indicating that a thread should be closed without stopping the scheduler."""
    pass