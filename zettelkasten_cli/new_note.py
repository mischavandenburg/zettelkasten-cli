import typer
from rich import print
from typing import Optional
from pathlib import Path
from zettelkasten_cli.config import MAX_TITLE_LENGTH, INBOX_PATH, PROMPT_TITLE
from zettelkasten_cli.utils import open_in_editor, format_from_vim
from zettelkasten_cli.daily_note import append_daily_note

app = typer.Typer()


def create_new_note(title) -> None:
    """Create a new note from the command line."""
    try:
        note_title = get_note_title(title)
        validate_title(note_title)
        file_path = format_path(note_title)
        create_and_open_file(file_path, note_title)
    except ValueError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)
    except FileExistsError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}", err=True)
        raise typer.Exit(code=1)


def get_note_title(title: Optional[str]) -> str:
    """Get the note title from input or prompt the user."""
    return title.strip() if title else typer.prompt(PROMPT_TITLE)


def validate_title(title: str) -> None:
    """Validate the note title."""
    if not title:
        raise ValueError("Note title cannot be empty.")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title cannot be more than {MAX_TITLE_LENGTH} characters.")
    if title.endswith(".md"):
        raise ValueError("Leave out the .md extension.")


def format_path(note_title: str) -> Path:
    """Format the absolute path based on Zettelkasten location and the note title."""
    return INBOX_PATH / f"{note_title}.md"


def create_and_open_file(file_path: Path, note_title: str) -> None:
    """Create a new note file and open it in the editor."""
    if file_path.exists():
        raise FileExistsError(f"The file already exists: {file_path}")
    create_note_file(file_path, note_title)
    print(f"New note created: {file_path}")
    open_in_editor(str(file_path))


def create_note_file(file_path: Path, note_title: str) -> None:
    """
    Create a new note file with the given title and add a H1 Markdown heading.
    """
    append_daily_note(note_title)
    file_path.write_text(f"# {note_title}\n\n")


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def new_note_from_vim(context: typer.Context) -> None:
    """Takes line from vim when sent with !! and creates it"""
    # TODO: Implement --vim option to pass text from vim with "- [[test]]" formatting
    try:
        file_name = format_from_vim(" ".join(context.args))
        print(file_name)
        # TODO: Implement the logic to add the link from the daily note
    except ValueError as e:
        print(f"Error: {str(e)}")
