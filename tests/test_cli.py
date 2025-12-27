"""Tests for zettelkasten-cli."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from zettelkasten_cli import __version__
from zettelkasten_cli.exceptions import (
    ConfigurationError,
    NoteExistsError,
    NoteTitleError,
)
from zettelkasten_cli.main import app


runner = CliRunner()


class TestVersion:
    """Test version."""

    def test_version_is_semver(self):
        """Version should be semantic versioning format."""
        parts = __version__.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)


class TestExceptions:
    """Test custom exceptions."""

    def test_configuration_error(self):
        """ConfigurationError should have a message."""
        error = ConfigurationError("test message")
        assert str(error) == "test message"

    def test_note_exists_error(self):
        """NoteExistsError should have a message."""
        error = NoteExistsError("note exists")
        assert str(error) == "note exists"

    def test_note_title_error(self):
        """NoteTitleError should have a message."""
        error = NoteTitleError("invalid title")
        assert str(error) == "invalid title"


class TestConfig:
    """Test configuration loading."""

    def test_missing_zettelkasten_env_raises_error(self):
        """Should raise ConfigurationError when ZETTELKASTEN is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove ZETTELKASTEN if it exists
            os.environ.pop("ZETTELKASTEN", None)

            from zettelkasten_cli.config import Config

            with pytest.raises(ConfigurationError):
                Config.load()

    def test_config_loads_with_valid_env(self, tmp_path: Path):
        """Should load config when ZETTELKASTEN is set to valid path."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}, clear=True):
            # Reset singleton
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.config import Config

            config = Config.load()
            assert config.paths.root == tmp_path


class TestCLI:
    """Test CLI commands."""

    def test_help_shows_commands(self):
        """Help should list available commands."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "new" in result.stdout
        assert "day" in result.stdout
        assert "week" in result.stdout

    def test_new_help(self):
        """New command should have help text."""
        result = runner.invoke(app, ["new", "--help"])
        assert result.exit_code == 0
        assert "Create a new note" in result.stdout

    def test_day_help(self):
        """Day command should have help text."""
        result = runner.invoke(app, ["day", "--help"])
        assert result.exit_code == 0
        assert "daily note" in result.stdout

    def test_week_help(self):
        """Week command should have help text."""
        result = runner.invoke(app, ["week", "--help"])
        assert result.exit_code == 0
        assert "weekly note" in result.stdout


class TestNote:
    """Test Note model."""

    def test_empty_title_raises_error(self, tmp_path: Path):
        """Empty title should raise NoteTitleError."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.config import get_config
            from zettelkasten_cli.models.note import Note

            config = get_config()

            with pytest.raises(NoteTitleError, match="cannot be empty"):
                Note(title="", config=config)

    def test_long_title_raises_error(self, tmp_path: Path):
        """Title over 80 chars should raise NoteTitleError."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.config import get_config
            from zettelkasten_cli.models.note import Note

            config = get_config()
            long_title = "a" * 81

            with pytest.raises(NoteTitleError, match="more than 80"):
                Note(title=long_title, config=config)

    def test_md_extension_raises_error(self, tmp_path: Path):
        """Title ending in .md should raise NoteTitleError."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.config import get_config
            from zettelkasten_cli.models.note import Note

            config = get_config()

            with pytest.raises(NoteTitleError, match="extension"):
                Note(title="test.md", config=config)


class TestPeriodicNote:
    """Test PeriodicNote model."""

    def test_daily_date_format(self, tmp_path: Path):
        """Daily note should use YYYY-MM-DD format."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.models.periodic_note import daily

            note = daily()
            date_str = note.get_current_date_str()

            # Should match YYYY-MM-DD pattern
            parts = date_str.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4  # Year
            assert len(parts[1]) == 2  # Month
            assert len(parts[2]) == 2  # Day

    def test_weekly_date_format(self, tmp_path: Path):
        """Weekly note should use YYYY-Www format."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.models.periodic_note import weekly

            note = weekly()
            date_str = note.get_current_date_str()

            # Should match YYYY-Www pattern
            assert "-W" in date_str
            parts = date_str.split("-W")
            assert len(parts) == 2
            assert len(parts[0]) == 4  # Year

    def test_daily_creates_note(self, tmp_path: Path):
        """Daily note should create file."""
        with patch.dict(os.environ, {"ZETTELKASTEN": str(tmp_path)}):
            import zettelkasten_cli.config as config_module

            config_module._config = None

            from zettelkasten_cli.models.periodic_note import daily

            note = daily()
            assert not note.exists()

            note.create()
            assert note.exists()
            assert note.note_path.read_text().startswith("#")
