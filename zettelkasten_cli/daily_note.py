import typer
from rich import print
import subprocess
from zettelkasten_cli.utils import format_date
from zettelkasten_cli.config import ZETTELKASTEN_ROOT

app = typer.Typer()

TODAY = format_date()
YESTERDAY = format_date(-1)
TOMORROW = format_date(1)

DAILY_NOTES_PATH = ZETTELKASTEN_ROOT / "periodic-notes" / "daily-notes"
TODAY_NOTE_PATH = DAILY_NOTES_PATH / f"{TODAY}.md"

# TODO: Add type hints


def create_daily_note(file_path):
    """Sets up the daily note template."""

    # TODO: set up template in separate file
    content = f"""
[[{YESTERDAY}]] - [[{TOMORROW}]]

## Daily Deeds

- [ ] Track calories
- [ ] Yoga
- [ ] Exercise
- [ ] Check Weekly Note for Intentions

## Journal
"""
    file_path.write_text(content)


def append_daily_note(note_title):
    """Append given note title to daily note as Obsidian markdown link."""
    with TODAY_NOTE_PATH.open(mode="a") as note:
        note.write(f"\n[[{note_title}]]")


def open_daily_note():
    """Create or open today's daily note."""

    if not TODAY_NOTE_PATH.exists():
        print(f"File does not exist, creating new daily note: {TODAY_NOTE_PATH}")
        create_daily_note(TODAY_NOTE_PATH)
    else:
        print(f"Opening existing daily note: {TODAY_NOTE_PATH}")

    # Open the file in Neovim at the bottom in insert mode and run NoNeckPain
    subprocess.run(["nvim", "+ normal Gzzo", str(TODAY_NOTE_PATH), "-c", ":NoNeckPain"])
