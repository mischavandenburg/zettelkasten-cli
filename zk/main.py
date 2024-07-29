import os
import re
import subprocess
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

# Constants
MAX_TITLE_LENGTH = 80
INBOX_PATH = "/Users/mischa/Zettelkasten/0 Inbox"
PROMPT_TITLE = "Enter the title of the note"


# Custom Exceptions
class EmptyTitleError(ValueError):
    """Raised when the note title is empty."""


class TitleTooLongError(ValueError):
    """Raised when the note title exceeds the maximum length."""


class FileExistsError(IOError):
    """Raised when trying to create a file that already exists."""


class InvalidInputError(ValueError):
    """Raised when the input doesn't match the expected format."""


app = typer.Typer()


@app.command()
def new(title: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """Create a new note from the command line."""
    try:
        note_title = get_note_title(title)
        validate_title(note_title)
        file_path = format_path(note_title)
        create_and_open_file(file_path, note_title)
    except (EmptyTitleError, TitleTooLongError, FileExistsError) as e:
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
        raise EmptyTitleError("Note title cannot be empty.")
    if len(title) > MAX_TITLE_LENGTH:
        raise TitleTooLongError(
            f"Title cannot be more than {MAX_TITLE_LENGTH} characters."
        )
    if title.endswith(".md"):
        raise ValueError("Leave out the .md extension.")


def format_path(note_title: str) -> str:
    """Format the absolute path based on Zettelkasten location and the note title."""
    return os.path.join(INBOX_PATH, f"{note_title}.md")


def create_note_file(file_path: str, note_title: str) -> None:
    """Create a new note file with the given title."""
    with open(file_path, "w") as f:
        f.write(f"# {note_title}\n\n")


def open_in_neovim(file_path: str) -> None:
    """Open the created file in Neovim."""
    try:
        subprocess.run(["nvim", file_path], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to open the file with nvim.")
    except FileNotFoundError:
        print(
            "Error: nvim command not found. Make sure it's installed and in your PATH."
        )


def create_and_open_file(file_path: str, note_title: str) -> None:
    """Create a new note file and open it in Neovim."""
    if os.path.exists(file_path):
        raise FileExistsError(f"The file already exists: {file_path}")

    create_note_file(file_path, note_title)
    print(f"New note created: {file_path}")
    open_in_neovim(file_path)


# To allow input like "- [[this is my new note]]", we need to allow extra args
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def new_note_from_vim(context: typer.Context) -> None:
    """Create new note and add link to daily note."""

    print(context.args)
    file_name = format_from_vim(" ".join(context.args))
    print(file_name)


def format_from_vim(input_line: str) -> str:
    """
    Extract file name from input line (expected format: '[[file name]]').

    Args:
        input_line (str): The input string containing the file name.

    Returns:
        str: The extracted file name with '.md' extension.

    Raises:
        InvalidInputError: If no text is found between double brackets.
    """
    match = re.search(r"\[\[(.*?)\]\]", input_line)
    if not match:
        raise InvalidInputError("No text found between double brackets")
    return f"{match.group(1)}.md"
