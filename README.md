# Zettelkasten CLI

A bespoke CLI for my Neovim + Obsidian Zettelkasten written in Python.

**Usage**:

```console
[OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `day`: Open daily note or create if it doesn't...
- `week`: Open weekly note or create if it doesn't...
- `new`: Create a new note with the provided title.

## `day`

Open daily note or create if it doesn't exist.

**Usage**:

```console
day [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## `new`

Create a new note with the provided title. Will prompt if no title given.
Adds Obsidian markdown link to the daily note.

**Usage**:

```console
new [OPTIONS] [TITLE]
```

**Arguments**:

- `[TITLE]`

**Options**:

- `--vim`: Indicates input is coming from vim. Prevents new file being opened.
- `--help`: Show this message and exit.

## Creating a Release

Push the changes to the repo and create a release with a new tag from the GitHub CLI or from the UI.

The GH Actions workflow handles the rest. It auto-updates the pyproject.toml and pushes to PyPi.

## Installing

1. Make sure the `pyproject.toml` is present in the root directory.
2. Add if not present:

```toml
[tool.poetry.scripts]
zk = "zettelkasten_cli.main:app"
```

3. Run `poetry build`. This will create the wheel file in the `dist/` directory.
4. `cd dist/`
5. Next, `pipx install dist/zettelkasten_cli-0.1.0-py3-none-any.whl`
6. If it doesn't exist, create a symlink to the `zk` command in your path: `ln -s ~/.local/share/pipx/venvs/zettelkasten-cli/bin/zk ~/.local/bin/`
7. Add `export ZETTELKASTEN=<path to directory>` to your shell profile. You can also specify the `ZETTELKASTEN_NVIM_ARGS` and `ZETTELKASTEN_NVIM_COMMANDS` environment variables if you prefer a different opening sequence.

Run `zk` to get started.

== OR ==

Simply run `poetry install && poetry run zk`
