import os
from pathlib import Path

# Paths
ZETTELKASTEN_ROOT = Path(os.environ.get("ZETTELKASTEN", ""))
INBOX_PATH = ZETTELKASTEN_ROOT / "0 Inbox"

# File settings
MAX_TITLE_LENGTH = 80

# Prompts
PROMPT_TITLE = "Enter the title of the note"

# Commands
EDITOR_COMMAND = "nvim"
