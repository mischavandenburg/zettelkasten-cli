import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

from rich import print

from zettelkasten_cli.config import EDITOR_COMMAND, NVIM_ARGS, NVIM_COMMANDS


def format_date(delta_days=0):
    return (datetime.now() + timedelta(days=delta_days)).strftime("%Y-%m-%d")


def format_week(delta_days=0):
    return (
        datetime.now() + timedelta(days=delta_days - datetime.now().weekday())
    ).strftime("%Y-W%V")


def open_in_editor(file_path: Union[str, Path]) -> None:
    """
    Open the file in the configured editor.
    """
    # Convert Path objects to strings if needed
    if isinstance(file_path, Path):
        file_path = str(file_path)

    try:
        if EDITOR_COMMAND == "nvim":
            cmd = ["nvim", NVIM_ARGS, file_path]

            # Add any additional commands
            for nvim_cmd in NVIM_COMMANDS:
                if nvim_cmd and nvim_cmd.strip():  # only add non-empty commands
                    cmd.extend(["-c", nvim_cmd.strip()])
        else:
            # For other editors, just use the basic command
            cmd = [EDITOR_COMMAND, file_path]

        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to open the file with {EDITOR_COMMAND}: {e}")
    except FileNotFoundError:
        print(
            f"Error: {EDITOR_COMMAND} command not found. Make sure it's installed and in your PATH."
        )
