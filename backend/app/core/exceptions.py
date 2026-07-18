class ResourceNotFoundError(Exception):
    """Raised when a requested resource does not exist."""


class DatabaseIntegrityError(Exception):
    """Raised when a database constraint prevents a write operation."""
