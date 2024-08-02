import re
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


def format_from_vim(input_line: str) -> str:
    """
    Extract file name from input line (expected format: '[[file name]]').
    """
    match = re.search(r"\[\[(.*?)\]\]", input_line)
    if not match:
        raise ValueError("No text found between double brackets")
    return f"{match.group(1)}.md"
