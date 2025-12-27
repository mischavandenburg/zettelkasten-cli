"""Custom exceptions for zettelkasten-cli."""


class ZettelkastenError(Exception):
    """Base exception for all zettelkasten-cli errors."""

    pass


class ConfigurationError(ZettelkastenError):
    """Raised when configuration is invalid or missing."""

    pass


class NoteExistsError(ZettelkastenError):
    """Raised when attempting to create a note that already exists."""

    pass


class NoteTitleError(ZettelkastenError):
    """Raised when note title is invalid."""

    pass


class TemplateError(ZettelkastenError):
    """Raised when template loading fails."""

    pass


class EditorError(ZettelkastenError):
    """Raised when editor operations fail."""

    pass
