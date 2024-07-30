import typer

from zk import new_note
from zk import day

from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()
app.add_typer(day.app, name="day")


@app.command()
def new(title: Annotated[Optional[str], typer.Argument()] = None) -> None:
    new_note.create_new_note(title)


# if __name__ == "__main__":
#     app()
#
