import os
import sys
from pathlib import Path

import typer
from rich import print as rich_print

from zettelkasten_cli.config import ZETTELKASTEN_ROOT
from zettelkasten_cli.utils import format_date, format_week, open_in_editor

app = typer.Typer()


def log(message: str) -> None:
    """Print message only if stdout is a TTY (not captured by another process)."""
    if sys.stdout.isatty():
        rich_print(message)

TODAY = format_date()
YESTERDAY = format_date(-1)
TOMORROW = format_date(1)
THIS_WEEK = format_week()
LAST_WEEK = format_week(-7)  # Correct this to start on Monday and end Sunday
NEXT_WEEK = format_week(7)  # Correct this to start on Monday and end Sunday
CONFIG_PATH = Path(os.environ.get("XDG_CONFIG_HOME", ""))

DAILY_NOTES_PATH = ZETTELKASTEN_ROOT / "periodic-notes" / "daily"
DAILY_NOTES_TEMPLATE_PATH = ZETTELKASTEN_ROOT / "zk" / "daily.md"
TODAY_NOTE_PATH = DAILY_NOTES_PATH / f"{TODAY}.md"

WEEKLY_NOTES_PATH = ZETTELKASTEN_ROOT / "periodic-notes" / "weekly"
WEEKLY_NOTES_TEMPLATE_PATH = ZETTELKASTEN_ROOT / "zk" / "weekly.md"
THIS_WEEK_NOTE_PATH = WEEKLY_NOTES_PATH / f"{THIS_WEEK}.md"


def format_daily_note_content() -> str:
    """
    Creates the daily note template content by reading from the template file.
    Returns:
        str: Formatted content for the daily note.
    """
    # Add the navigation links at the top
    content = f"[[{YESTERDAY}]] - [[{TOMORROW}]]\n\n"

    # Read and append the template content if it exists
    try:
        if DAILY_NOTES_TEMPLATE_PATH.exists():
            template_content = DAILY_NOTES_TEMPLATE_PATH.read_text()
            content += template_content
        else:
            log(f"Warning: Template file not found at {DAILY_NOTES_TEMPLATE_PATH}")
            # Fallback to default template
            content += """
## Journal

"""
    except IOError as e:
        log(f"Error reading template file: {e}")
        # Fallback to default template
        content += """
## Journal
"""

    return content


def format_weekly_note_content() -> str:
    """
    Creates the weekly note template content by reading from the template file.
    Returns:
        str: Formatted content for the weekly note.
    """
    # Read and append the template content if it exists
    content = f"[[{LAST_WEEK}]] - [[{NEXT_WEEK}]]\n\n"

    try:
        if WEEKLY_NOTES_TEMPLATE_PATH.exists():
            template_content = WEEKLY_NOTES_TEMPLATE_PATH.read_text()
            content += template_content
        else:
            log(f"Warning: Template file not found at {WEEKLY_NOTES_TEMPLATE_PATH}")
            # Fallback to default template
            content += """
## Weekly Journal

"""
    except IOError as e:
        log(f"Error reading template file: {e}")
        # Fallback to default template
        content += """
### Weekly Journal
"""
    return content


def create_daily_note() -> None:
    """
    Creates the daily note if it doesn't exist.
    If the note already exists, it prints a message indicating so.
    """
    try:
        if not TODAY_NOTE_PATH.exists():
            log(f"Creating new daily note: {TODAY_NOTE_PATH}")
            TODAY_NOTE_PATH.write_text(format_daily_note_content())
        else:
            log(f"Daily note already exists: {TODAY_NOTE_PATH}")
    except IOError as e:
        log(f"Error creating daily note: {e}")


def append_daily_note(note_title: str) -> None:
    """
    Appends given note title to daily note as Obsidian markdown link.
    Args:
        note_title (str): The title of the note to be appended.
    """
    create_daily_note()
    try:
        with TODAY_NOTE_PATH.open(mode="a") as note:
            note.write(f"\n[[{note_title}]]")
    except IOError as e:
        log(f"Error appending to daily note: {e}")


def open_daily_note() -> None:
    """
    Opens today's daily note in Neovim.
    Creates the note if it doesn't exist before opening.
    """
    create_daily_note()
    try:
        open_in_editor(TODAY_NOTE_PATH)
    except Exception as e:
        log(f"Error opening daily note: {e}")


def create_weekly_note() -> None:
    """
    Creates the weekly note if it doesn't exist.
    """
    try:
        if not THIS_WEEK_NOTE_PATH.exists():
            log(f"Creating new weekly note: {WEEKLY_NOTES_PATH}")
            THIS_WEEK_NOTE_PATH.write_text(format_weekly_note_content())
        else:
            log(f"Weekly note already exists: {WEEKLY_NOTES_PATH}")
    except IOError as e:
        log(f"Error creating weekly note: {e}")


def append_weekly_note(note_title: str) -> None:
    """
    Appends given note title to weekly note as Obsidian markdown link.
    Args:
        note_title (str): The title of the note to be appended.
    """
    create_weekly_note()
    try:
        with WEEKLY_NOTES_PATH.open(mode="a") as note:
            note.write(f"\n[[{note_title}]]")
    except IOError as e:
        log(f"Error appending to weekly note: {e}")


def open_weekly_note() -> None:
    """
    Opens this week's weekly note in Neovim.
    If the note doesn't exist, it prints an error message.
    """
    create_weekly_note()
    try:
        open_in_editor(THIS_WEEK_NOTE_PATH)
    except Exception as e:
        log(f"Error opening weekly note: {e}")
