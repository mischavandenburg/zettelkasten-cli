from pathlib import Path
import os

# Paths
ZETTELKASTEN_ROOT = Path(os.environ.get("~/Documents/Obsidian_Vault", ""))
INBOX_PATH = ZETTELKASTEN_ROOT / "1_Fleeting_Notes"

# File settings
MAX_TITLE_LENGTH = 80

# Prompts
PROMPT_TITLE = "Enter the title of the note"

# Commands
EDITOR_COMMAND = "nvim"
