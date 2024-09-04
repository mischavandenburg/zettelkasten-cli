import typer
from rich import print
import subprocess
from zettelkasten_cli.utils import format_date
from zettelkasten_cli.config import ZETTELKASTEN_ROOT
from datetime import datetime
from pathlib import Path

app = typer.Typer()

TODAY = format_date()
YESTERDAY = format_date(-1)
TOMORROW = format_date(1)
DAILY_NOTES_PATH = ZETTELKASTEN_ROOT / "periodic-notes" / "daily-notes"
TODAY_NOTE_PATH = DAILY_NOTES_PATH / f"{TODAY}.md"
WEEKLY_NOTES_PATH = ZETTELKASTEN_ROOT / "periodic-notes" / "weekly-notes"


def format_daily_note_content() -> str:
    """
    Creates the daily note template content.

    Returns:
        str: Formatted content for the daily note.
    """
    # TODO: Consider moving this template to a separate config file
    return f"""
[[{YESTERDAY}]] - [[{TOMORROW}]]

## Daily Deeds

- [ ] Track calories
- [ ] Yoga
- [ ] Exercise
- [ ] Check Weekly Note for Intentions

## Journal

"""


def create_daily_note() -> None:
    """
    Creates the daily note if it doesn't exist.
    If the note already exists, it prints a message indicating so.
    """
    try:
        if not TODAY_NOTE_PATH.exists():
            print(f"Creating new daily note: {TODAY_NOTE_PATH}")
            TODAY_NOTE_PATH.write_text(format_daily_note_content())
        else:
            print(f"Daily note already exists: {TODAY_NOTE_PATH}")
    except IOError as e:
        print(f"Error creating daily note: {e}")


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
        print(f"Error appending to daily note: {e}")


def open_daily_note() -> None:
    """
    Opens today's daily note in Neovim.
    Creates the note if it doesn't exist before opening.
    """

    # TODO: use the function from utils
    create_daily_note()
    try:
        subprocess.run(
            ["nvim", "+ normal Gzzo", str(TODAY_NOTE_PATH), "-c", ":NoNeckPain"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error opening daily note in Neovim: {e}")


def get_weekly_note_path() -> Path:
    """
    Formats the note title.
    Returns the path to the current week's note.
    """
    week_number = datetime.now().strftime("%Y-W%W")
    return WEEKLY_NOTES_PATH / f"{week_number}.md"

    # TODO: use the function from utils


@app.command()
def open_weekly_note():
    """
    Opens this week's weekly note in Neovim if it exists.
    If the note doesn't exist, it prints an error message.
    """
    weekly_note_path = get_weekly_note_path()

    if not weekly_note_path.exists():
        print(
            "[bold red]Error:[/bold red] Weekly note doesn't exist. Please create it in Obsidian."
        )
        return

    try:
        subprocess.run(
            ["nvim", "+ normal Gzzo", str(weekly_note_path), "-c", ":NoNeckPain"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error opening weekly note in Neovim: {e}")
