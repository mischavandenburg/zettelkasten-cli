import subprocess
from rich import print
from zettelkasten_cli.config import EDITOR_COMMAND
from datetime import datetime, timedelta


def format_date(delta_days=0):
    return (datetime.now() + timedelta(days=delta_days)).strftime("%Y-%m-%d")


def open_in_editor(file_path: str) -> None:
    """Open the created file in the configured editor."""
    try:
        subprocess.run([EDITOR_COMMAND, file_path], check=True)
    except subprocess.CalledProcessError:
        print(f"Error: Failed to open the file with {EDITOR_COMMAND}.")
    except FileNotFoundError:
        print(
            f"Error: {EDITOR_COMMAND} command not found. Make sure it's installed and in your PATH."
        )
