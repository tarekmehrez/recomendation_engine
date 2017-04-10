"""Contains package-specific exception classes."""


class RequiredConfigOptionNotFoundError(Exception):

    """Required config option not found error."""

    pass


class FormatNotSupportedError(Exception):

    """Format not supported exception while doing io operations."""
    pass


class LanguageNotSupportedError(Exception):

    """Language not supported error."""
    pass


class IllegalArgumentError(Exception):

    """Passing wrong arguments."""
    pass
