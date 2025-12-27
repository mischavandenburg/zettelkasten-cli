"""CLI entry point for zettelkasten-cli."""

from typing import Optional

import typer
from typing_extensions import Annotated

from zettelkasten_cli import output
from zettelkasten_cli.exceptions import (
    ConfigurationError,
    NoteExistsError,
    NoteTitleError,
    ZettelkastenError,
)
from zettelkasten_cli.models.note import create_note
from zettelkasten_cli.models.periodic_note import daily, weekly

app = typer.Typer(
    name="zk",
    help="A CLI for managing your Neovim + Obsidian Zettelkasten.",
    no_args_is_help=True,
)


def handle_error(e: Exception) -> None:
    """Handle exceptions and exit with appropriate code."""
    if isinstance(e, ConfigurationError):
        output.error(f"Configuration error: {e}")
        raise typer.Exit(code=2)
    elif isinstance(e, (NoteExistsError, NoteTitleError)):
        output.error(str(e))
        raise typer.Exit(code=1)
    elif isinstance(e, ZettelkastenError):
        output.error(str(e))
        raise typer.Exit(code=1)
    else:
        output.error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@app.command()
def new(
    title: Annotated[Optional[str], typer.Argument(help="Note title")] = None,
    vim: Annotated[
        bool, typer.Option("--vim", help="Output path for Neovim integration")
    ] = False,
) -> None:
    """
    Create a new note in the inbox.

    If no title is provided, you will be prompted to enter one.
    The note is automatically linked in today's daily note.
    """
    try:
        # Prompt for title if not provided
        if not title:
            title = typer.prompt("Enter note title")

        create_note(title=title.strip(), vim_mode=vim)

    except Exception as e:
        handle_error(e)


@app.command()
def day() -> None:
    """
    Open today's daily note.

    Creates the note if it doesn't exist.
    """
    try:
        daily().open()
    except Exception as e:
        handle_error(e)


@app.command()
def week() -> None:
    """
    Open this week's weekly note.

    Creates the note if it doesn't exist.
    """
    try:
        weekly().open()
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    app()
