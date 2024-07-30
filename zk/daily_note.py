import typer
from rich import print
from datetime import datetime, timedelta
from pathlib import Path
import os
import subprocess

app = typer.Typer()

# Assuming ZETTELKASTEN is an environment variable, we'll get it like this:
ZETTELKASTEN = Path(os.environ.get("ZETTELKASTEN", ""))
DAILY_NOTES_PATH = ZETTELKASTEN / "periodic-notes" / "daily-notes"


def get_date_string(delta_days=0):
    return (datetime.now() + timedelta(days=delta_days)).strftime("%Y-%m-%d")


def format_daily_note(file_path, yesterday, tomorrow):
    """Sets up the daily note template."""

    # TODO: set up template in separate file
    content = f"""
[[{yesterday}]] - [[{tomorrow}]]
## Habits
- [ ] Calorie logging
- [ ] Yoga
- [ ] Exercise
## Log
"""
    file_path.write_text(content)


def open_daily_note():
    """Create or open today's daily note."""
    today = get_date_string()
    yesterday = get_date_string(-1)
    tomorrow = get_date_string(1)

    file_path = DAILY_NOTES_PATH / f"{today}.md"

    if not file_path.exists():
        print(f"File does not exist, creating new daily note: {file_path}")
        format_daily_note(file_path, yesterday, tomorrow)
    else:
        print(f"Opening existing daily note: {file_path}")

    # Change to the ZETTELKASTEN directory
    os.chdir(ZETTELKASTEN)

    # Open the file in Neovim at the bottom in insert mode and run NoNeckPain
    subprocess.run(["nvim", "+ normal Gzzo", str(file_path), "-c", ":NoNeckPain"])
