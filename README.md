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

- `--help`: Show this message and exit.
