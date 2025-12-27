import os
from pathlib import Path

# Paths
ZETTELKASTEN_ROOT = Path(os.environ.get("ZETTELKASTEN", ""))

# Inbox directory (configurable via environment variable)
INBOX_DIR = os.environ.get("ZETTELKASTEN_INBOX_DIR", "0 Inbox")
INBOX_PATH = ZETTELKASTEN_ROOT / INBOX_DIR

# Periodic notes paths (configurable via environment variables)
DAILY_NOTES_DIR = os.environ.get("ZETTELKASTEN_DAILY_DIR", "periodic-notes/daily-notes")
WEEKLY_NOTES_DIR = os.environ.get("ZETTELKASTEN_WEEKLY_DIR", "periodic-notes/weekly-notes")

DAILY_NOTES_PATH = ZETTELKASTEN_ROOT / DAILY_NOTES_DIR
WEEKLY_NOTES_PATH = ZETTELKASTEN_ROOT / WEEKLY_NOTES_DIR

# Template paths (configurable via environment variables)
DAILY_TEMPLATE_PATH = os.environ.get("ZETTELKASTEN_DAILY_TEMPLATE", "zk/daily.md")
WEEKLY_TEMPLATE_PATH = os.environ.get("ZETTELKASTEN_WEEKLY_TEMPLATE", "zk/weekly.md")

DAILY_NOTES_TEMPLATE_PATH = ZETTELKASTEN_ROOT / DAILY_TEMPLATE_PATH
WEEKLY_NOTES_TEMPLATE_PATH = ZETTELKASTEN_ROOT / WEEKLY_TEMPLATE_PATH

# File settings
MAX_TITLE_LENGTH = 80

# Prompts
PROMPT_TITLE = "Enter the title of the note"

# Editor (configurable via environment variable)
EDITOR_COMMAND = os.environ.get("ZETTELKASTEN_EDITOR", "nvim")

# Only use default arguments if environment variable is not set
NVIM_ARGS = os.environ.get("ZETTELKASTEN_NVIM_ARGS") or "+ normal Gzzo"

# Only use default commands if environment variable is not set
nvim_cmds = os.environ.get("ZETTELKASTEN_NVIM_COMMANDS")
NVIM_COMMANDS = nvim_cmds.split(",") if nvim_cmds else [":NoNeckPain"]
