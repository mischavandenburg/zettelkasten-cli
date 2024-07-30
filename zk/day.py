import typer
from rich import print

app = typer.Typer()


@app.command()
def daywrite():
    print("test from day")
