"""Template service for loading note templates."""

from pathlib import Path

from zettelkasten_cli import output


def load_template(template_path: Path) -> str | None:
    """
    Load a template from the given path.

    Args:
        template_path: Path to the template file.

    Returns:
        Template content if file exists, None otherwise.
    """
    try:
        if template_path.exists():
            return template_path.read_text()
    except OSError as e:
        output.warning(f"Could not read template {template_path}: {e}")

    return None
