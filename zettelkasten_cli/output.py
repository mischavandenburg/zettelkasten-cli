"""Unified output handling for zettelkasten-cli."""

import sys

from rich.console import Console

# Rich console for styled output
_console = Console()


def is_interactive() -> bool:
    """Check if stdout is connected to a terminal."""
    return sys.stdout.isatty()


def info(message: str) -> None:
    """Print an info message (only in interactive mode)."""
    if is_interactive():
        _console.print(message)


def success(message: str) -> None:
    """Print a success message (only in interactive mode)."""
    if is_interactive():
        _console.print(f"[green]{message}[/green]")


def warning(message: str) -> None:
    """Print a warning message (only in interactive mode)."""
    if is_interactive():
        _console.print(f"[yellow]{message}[/yellow]")


def error(message: str) -> None:
    """Print an error message (always, to stderr)."""
    _console.print(f"[red]{message}[/red]", stderr=True)


def plain(message: str) -> None:
    """Print a plain message without formatting (for piping to other programs)."""
    print(message, file=sys.stdout, flush=True)
