import typer
import sys
import os
import re
from rich import print
import subprocess

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def new(input: Annotated[Optional[str], typer.Argument()] = None):
    """
    Create a new note from the command line.
    Optional argument
    """

    if input is None or input.strip() == "":
        # If no input is provided or it's empty, prompt the user
        note_title = typer.prompt("Enter the title of the note")
    else:
        # Use the provided input as the note title
        note_title = input.strip()

    validate_title(note_title)

    # Ensure note_title is not empty after prompting
    if note_title.strip() == "":
        typer.echo("Error: Note title cannot be empty.")
        raise typer.Exit(code=1)
    file = format_path(note_title)

    open_file(file, note_title)


def validate_title(title: str):
    if len(title) > 80:
        print("Title can not be more than 80 characters.")
        sys.exit(1)

    if title.endswith(".md"):
        print("Leave out the .md extension.")
        sys.exit(1)


def format_path(note_title: str) -> str:
    """
    Formats the absolute path based on Zettelkasten location and the note title.
    """
    inbox = "/Users/mischa/Zettelkasten/0 Inbox"
    file_name = f"{note_title}.md"
    file_path = os.path.join(inbox, file_name)

    print(file_path)
    return file_path


def open_file(file: str, note_title: str):
    """
    Opens the file in Neovim
    """
    if os.path.exists(file):
        print("The file already exists.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file, "w") as f:
            # Add the title of the file as H1 markdown heading
            f.write(f"# {note_title}\n\n")

        print(f"New note created: {file}")

        try:
            subprocess.run(["nvim", file], check=True)

        except subprocess.CalledProcessError:
            print("Error: Failed to open the file with nvim.")

        except FileNotFoundError:
            print(
                "Error: nvim command not found. Make sure it's installed and in your PATH."
            )
    except IOError as e:
        print(f"Error creating note: {e}")
        sys.exit(1)


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
