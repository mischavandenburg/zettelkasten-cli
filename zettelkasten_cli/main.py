import typer

from zettelkasten_cli import new_note
from zettelkasten_cli import periodic_notes

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def new(
    title: Annotated[Optional[str], typer.Argument()] = None,
    vim_mode: Annotated[bool, typer.Option("--vim")] = False,
) -> None:
    """Create a new note with the provided title. Will prompt if no title given.
    Adds Obsidian markdown link to the daily note.
    """
    new_note.create_new_note(title, vim_mode)


@app.command()
def day():
    """Open daily note or create if it doesn't exist."""
    periodic_notes.open_daily_note()


@app.command()
def week():
    """Open weekly note or throw error if it doesn't exist."""
    periodic_notes.open_weekly_note()
