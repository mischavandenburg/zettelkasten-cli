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

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ZETTELKASTEN` | Yes | - | Path to your Zettelkasten root directory |
| `ZETTELKASTEN_NVIM_ARGS` | No | `+ normal Gzzo` | Arguments passed to Neovim when opening notes |
| `ZETTELKASTEN_NVIM_COMMANDS` | No | `:NoNeckPain` | Comma-separated Neovim commands to run on open |

Add to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
export ZETTELKASTEN="$HOME/Documents/Zettelkasten"

# Optional: customize Neovim behavior
export ZETTELKASTEN_NVIM_ARGS="+ normal Gzzo"
export ZETTELKASTEN_NVIM_COMMANDS=":NoNeckPain,:set wrap"
```

### Expected Directory Structure

The CLI expects the following structure within your `ZETTELKASTEN` directory:

```
$ZETTELKASTEN/
├── 0 Inbox/              # New notes are created here
├── periodic-notes/
│   ├── daily/            # Daily notes (YYYY-MM-DD.md)
│   └── weekly/           # Weekly notes (YYYY-Www.md)
└── zk/
    ├── daily.md          # Template for daily notes
    └── weekly.md         # Template for weekly notes
```

### Templates

Daily and weekly note templates are read from the `zk/` directory. If templates don't exist, minimal defaults are used.

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
