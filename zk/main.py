from sre_constants import error
import typer
import sys
import os
import re
from rich import print
import subprocess

from typing import Optional
from typing_extensions import Annotated


ERROR_EMPTY_TITLE = "Error: Note title cannot be empty."
PROMPT_TITLE = "Enter the title of the note"
MAX_TITLE_LENGTH = 80
INBOX_PATH = "/Users/mischa/Zettelkasten/0 Inbox"

app = typer.Typer()


@app.command()
def new(input: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """
    Create a new note from the command line.
    The argument is optional, and the program will prompt when no title is given.
    """
    try:
        note_title = get_note_title(input)
        validate_title(note_title)

        file_path = format_path(note_title)
        open_file(file_path, note_title)

    except ValueError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}", err=True)
        raise typer.Exit(code=1)


def get_note_title(input: Optional[str]) -> str:
    """Get the note title from input or prompt the user."""
    if not input or input.strip() == "":
        return typer.prompt("Enter the title of the note")
    return input.strip()


def validate_title(title: str) -> None:
    """Validate the note title."""
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title cannot be more than {MAX_TITLE_LENGTH} characters.")
    if title.endswith(".md"):
        raise ValueError("Leave out the .md extension.")
    if not title.strip():
        raise ValueError(ERROR_EMPTY_TITLE)


def format_path(note_title: str) -> str:
    """
    Formats the absolute path based on Zettelkasten location and the note title.
    """
    file_name = f"{note_title}.md"
    return os.path.join(INBOX_PATH, file_name)


def create_note_file(file_path: str, note_title: str):
    with open(file_path, "w") as f:
        f.write(f"# {note_title}\n\n")


def open_in_neovim(file_path: str):
    try:
        subprocess.run(["nvim", file_path], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to open the file with nvim.")
    except FileNotFoundError:
        print(
            "Error: nvim command not found. Make sure it's installed and in your PATH."
        )


def open_file(file_path: str, note_title: str):
    if os.path.exists(file_path):
        raise FileExistsError(f"The file already exists: {file_path}")

    try:
        create_note_file(file_path, note_title)
        print(f"New note created: {file_path}")
        open_in_neovim(file_path)
    except IOError as e:
        print(f"Error creating note: {e}")
        raise


# To allow input like "- [[this is my new note]]", we need to allow extra args
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def new_note_from_vim(ctx: typer.Context):
    """
    Create new note and add link to daily note.
    """
    print(ctx.args)

    file_name = format_from_vim(" ".join(ctx.args))

    print(file_name)


def format_from_vim(input_line) -> str:
    match = re.search(r"\[\[(.*?)\]\]", input_line)
    if not match:
        print("Error: No text found between double brackets", file=sys.stderr)
        sys.exit(1)

    file_name = f"{match.group(1)}.md"
    return file_name
