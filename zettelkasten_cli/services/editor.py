"""Editor service for opening files."""

import subprocess
from pathlib import Path

from zettelkasten_cli.config import EditorConfig, get_config
from zettelkasten_cli.exceptions import EditorError


def open_in_editor(file_path: Path, config: EditorConfig | None = None) -> None:
    """
    Open a file in the configured editor.

    Args:
        file_path: Path to the file to open.
        config: Optional editor config (uses global config if not provided).

    Raises:
        EditorError: If the editor fails to open the file.
    """
    if config is None:
        config = get_config().editor

    cmd = _build_command(file_path, config)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise EditorError(f"Editor exited with error: {e}") from e
    except FileNotFoundError:
        raise EditorError(
            f"Editor '{config.command}' not found. "
            f"Make sure it's installed and in your PATH."
        ) from None


def _build_command(file_path: Path, config: EditorConfig) -> list[str]:
    """Build the command list for the editor."""
    if config.is_nvim:
        cmd = [config.command, config.nvim_args, str(file_path)]
        for nvim_cmd in config.nvim_commands:
            cmd.extend(["-c", nvim_cmd])
        return cmd

    return [config.command, str(file_path)]
