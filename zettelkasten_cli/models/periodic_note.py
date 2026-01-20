"""Periodic note model for daily, weekly, monthly, yearly notes."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

from zettelkasten_cli import output
from zettelkasten_cli.config import Config, get_config
from zettelkasten_cli.services.editor import open_in_editor
from zettelkasten_cli.services.template import load_template


class Period(Enum):
    """Periodic note period types."""

    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class PeriodicNote:
    """
    A periodic note (daily, weekly, etc.).

    This class encapsulates all logic for creating, opening, and appending
    to periodic notes, eliminating duplication between daily/weekly handling.
    """

    period: Period
    config: Config

    def get_current_date_str(self) -> str:
        """Get the formatted date string for the current period."""
        now = datetime.now()

        if self.period == Period.DAILY:
            return now.strftime("%Y-%m-%d")
        elif self.period == Period.WEEKLY:
            # Get Monday of current week
            monday = now - timedelta(days=now.weekday())
            return monday.strftime("%Y-W%V")

        raise ValueError(f"Unknown period: {self.period}")

    def get_offset_date_str(self, offset: int) -> str:
        """Get the formatted date string with an offset (e.g., -1 for yesterday)."""
        now = datetime.now()

        if self.period == Period.DAILY:
            target = now + timedelta(days=offset)
            return target.strftime("%Y-%m-%d")
        elif self.period == Period.WEEKLY:
            # Offset is in weeks
            monday = now - timedelta(days=now.weekday())
            target = monday + timedelta(weeks=offset)
            return target.strftime("%Y-W%V")

        raise ValueError(f"Unknown period: {self.period}")

    @property
    def notes_dir(self) -> Path:
        """Get the directory for this period's notes."""
        if self.period == Period.DAILY:
            return self.config.paths.daily_notes
        elif self.period == Period.WEEKLY:
            return self.config.paths.weekly_notes

        raise ValueError(f"Unknown period: {self.period}")

    @property
    def template_path(self) -> Path:
        """Get the template path for this period."""
        if self.period == Period.DAILY:
            return self.config.paths.daily_template_path
        elif self.period == Period.WEEKLY:
            return self.config.paths.weekly_template_path

        raise ValueError(f"Unknown period: {self.period}")

    @property
    def note_path(self) -> Path:
        """Get the full path to the current period's note."""
        return self.notes_dir / f"{self.get_current_date_str()}.md"

    def exists(self) -> bool:
        """Check if the current period's note exists."""
        return self.note_path.exists()

    def get_default_content(self) -> str:
        """Get the default content for a new note."""
        yesterday = self.get_offset_date_str(-1)
        tomorrow = self.get_offset_date_str(1)
        return f"# [[{yesterday}]] - [[{tomorrow}]]\n\n"

    def get_content(self) -> str:
        """Get the content for a new note (template or default)."""
        template_content = load_template(self.template_path)
        if template_content:
            return template_content

        return self.get_default_content()

    def create(self) -> bool:
        """
        Create the note if it doesn't exist.

        Returns:
            True if note was created, False if it already existed.
        """
        if self.exists():
            output.info(f"{self.period.value.title()} note already exists: {self.note_path}")
            return False

        # Ensure directory exists
        self.notes_dir.mkdir(parents=True, exist_ok=True)

        # Write the note
        self.note_path.write_text(self.get_content())
        output.info(f"Created {self.period.value} note: {self.note_path}")
        return True

    def open(self) -> None:
        """Create (if needed) and open the note in the editor."""
        self.create()
        open_in_editor(self.note_path, self.config.editor)

    def append(self, text: str) -> None:
        """
        Append text to the note.

        Creates the note first if it doesn't exist.
        """
        self.create()

        with self.note_path.open(mode="a") as f:
            f.write(text)


def daily(config: Config | None = None) -> PeriodicNote:
    """Create a daily note instance."""
    if config is None:
        config = get_config()
    return PeriodicNote(period=Period.DAILY, config=config)


def weekly(config: Config | None = None) -> PeriodicNote:
    """Create a weekly note instance."""
    if config is None:
        config = get_config()
    return PeriodicNote(period=Period.WEEKLY, config=config)
