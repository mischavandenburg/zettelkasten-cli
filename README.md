# Zettelkasten CLI

A bespoke CLI for my Neovim + Obsidian Zettelkasten written in Python.

## Installation

### From PyPI

```bash
pip install zettelkasten-cli
```

Or with uv:

```bash
uv tool install zettelkasten-cli
```

### From Source

```bash
git clone https://github.com/mischavandenburg/zettelkasten-cli.git
cd zettelkasten-cli
uv sync
uv run zk --help
```

## Configuration

Set the `ZETTELKASTEN` environment variable to your Zettelkasten root directory:

```bash
export ZETTELKASTEN=<path to directory>
```

Optional environment variables:
- `ZETTELKASTEN_NVIM_ARGS` - Custom Neovim arguments
- `ZETTELKASTEN_NVIM_COMMANDS` - Custom Neovim commands to run on open

## Usage

```console
zk [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell.
- `--help`: Show this message and exit.

**Commands**:

- `day`: Open daily note or create if it doesn't exist.
- `week`: Open weekly note or create if it doesn't exist.
- `new`: Create a new note with the provided title.

### `zk day`

Open daily note or create if it doesn't exist.

```console
zk day [OPTIONS]
```

### `zk week`

Open weekly note or create if it doesn't exist.

```console
zk week [OPTIONS]
```

### `zk new`

Create a new note with the provided title. Will prompt if no title given.
Adds Obsidian markdown link to the daily note.

```console
zk new [OPTIONS] [TITLE]
```

**Arguments**:

- `[TITLE]` - Note title (optional, will prompt if not provided)

**Options**:

- `--vim`: Indicates input is coming from Neovim. Suppresses rich output.

## Development

```bash
# Install dependencies
uv sync

# Run linter
uv run ruff check .

# Run tests
uv run pytest

# Build package
uv build
```

## Releasing

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases.

1. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:
   - `feat:` for new features (bumps minor version)
   - `fix:` for bug fixes (bumps patch version)
   - `feat!:` or `fix!:` for breaking changes (bumps major version)

2. When commits are pushed to main, release-please creates/updates a release PR

3. Merging the release PR automatically:
   - Creates a GitHub release with changelog
   - Publishes to PyPI
