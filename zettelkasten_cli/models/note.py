"""Note model for creating new notes in the inbox."""

from dataclasses import dataclass
from pathlib import Path

from zettelkasten_cli import output
from zettelkasten_cli.config import Config, get_config
from zettelkasten_cli.exceptions import NoteExistsError, NoteTitleError
from zettelkasten_cli.models.periodic_note import daily
from zettelkasten_cli.services.editor import open_in_editor

# Constraints
MAX_TITLE_LENGTH = 80


@dataclass
class Note:
    """
    A note in the Zettelkasten inbox.

    Handles creation, validation, and linking to daily notes.
    """

    title: str
    config: Config

    def __post_init__(self) -> None:
        """Validate the note after initialization."""
        self._validate_title()

    def _validate_title(self) -> None:
        """Validate the note title."""
        if not self.title:
            raise NoteTitleError("Note title cannot be empty.")

        if len(self.title) > MAX_TITLE_LENGTH:
            raise NoteTitleError(
                f"Title cannot be more than {MAX_TITLE_LENGTH} characters."
            )

        if self.title.endswith(".md"):
            raise NoteTitleError("Leave out the .md extension.")

    @property
    def path(self) -> Path:
        """Get the full path to the note file."""
        return self.config.paths.inbox / f"{self.title}.md"

    def exists(self) -> bool:
        """Check if the note already exists."""
        return self.path.exists()

    def get_content(self) -> str:
        """Get the initial content for the note."""
        return f"# {self.title}\n\n"

    def create(self, link_to_daily: bool = True) -> Path:
        """
        Create the note file.

        Args:
            link_to_daily: If True, add a link to the daily note.

        Returns:
            Path to the created note.

        Raises:
            NoteExistsError: If the note already exists.
        """
        if self.exists():
            raise NoteExistsError(f"Note already exists: {self.path}")

        # Ensure inbox directory exists
        self.config.paths.inbox.mkdir(parents=True, exist_ok=True)

        # Link to daily note first (so it appears even if note creation fails)
        if link_to_daily:
            daily_note = daily(self.config)
            daily_note.append(f"\n[[{self.title}]]")

        # Write the note
        self.path.write_text(self.get_content())

        return self.path

    def create_and_open(self, vim_mode: bool = False) -> None:
        """
        Create the note and open it in the editor.

        Args:
            vim_mode: If True, output plain text for Neovim integration.
        """
        path = self.create()

        if vim_mode:
            # Plain output for Neovim to parse
            output.plain(str(path))
        else:
            output.success(f"Created note: {path}")
            open_in_editor(path, self.config.editor)


def create_note(
    title: str,
    vim_mode: bool = False,
    config: Config | None = None,
) -> None:
    """
    Create a new note with the given title.

    Args:
        title: The note title.
        vim_mode: If True, output plain text for Neovim integration.
        config: Optional config (uses global if not provided).
    """
    if config is None:
        config = get_config()

    note = Note(title=title, config=config)
    note.create_and_open(vim_mode=vim_mode)
