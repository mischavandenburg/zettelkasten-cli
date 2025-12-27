"""Configuration management using dataclasses."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from zettelkasten_cli.exceptions import ConfigurationError


def _get_env(key: str, default: str | None = None) -> str | None:
    """Get environment variable value."""
    return os.environ.get(key, default)


def _get_env_required(key: str) -> str:
    """Get required environment variable, raise if missing."""
    value = os.environ.get(key)
    if not value:
        raise ConfigurationError(
            f"Environment variable {key} is required. "
            f"Set it to your Zettelkasten root directory."
        )
    return value


@dataclass(frozen=True)
class EditorConfig:
    """Editor configuration."""

    command: str = field(
        default_factory=lambda: _get_env("ZETTELKASTEN_EDITOR", "nvim") or "nvim"
    )
    nvim_args: str = field(
        default_factory=lambda: _get_env("ZETTELKASTEN_NVIM_ARGS", "+ normal Gzzo")
        or "+ normal Gzzo"
    )
    nvim_commands: list[str] = field(default_factory=lambda: _parse_nvim_commands())

    @property
    def is_nvim(self) -> bool:
        """Check if using neovim."""
        return self.command in ("nvim", "neovim")


def _parse_nvim_commands() -> list[str]:
    """Parse comma-separated nvim commands from env."""
    raw = _get_env("ZETTELKASTEN_NVIM_COMMANDS")
    if raw:
        return [cmd.strip() for cmd in raw.split(",") if cmd.strip()]
    return [":NoNeckPain"]


@dataclass(frozen=True)
class PathConfig:
    """Path configuration for the Zettelkasten."""

    root: Path
    inbox_dir: str = field(
        default_factory=lambda: _get_env("ZETTELKASTEN_INBOX_DIR", "0 Inbox")
        or "0 Inbox"
    )
    daily_dir: str = field(
        default_factory=lambda: _get_env(
            "ZETTELKASTEN_DAILY_DIR", "periodic-notes/daily-notes"
        )
        or "periodic-notes/daily-notes"
    )
    weekly_dir: str = field(
        default_factory=lambda: _get_env(
            "ZETTELKASTEN_WEEKLY_DIR", "periodic-notes/weekly-notes"
        )
        or "periodic-notes/weekly-notes"
    )
    daily_template: str = field(
        default_factory=lambda: _get_env("ZETTELKASTEN_DAILY_TEMPLATE", "zk/daily.md")
        or "zk/daily.md"
    )
    weekly_template: str = field(
        default_factory=lambda: _get_env("ZETTELKASTEN_WEEKLY_TEMPLATE", "zk/weekly.md")
        or "zk/weekly.md"
    )

    @property
    def inbox(self) -> Path:
        """Full path to inbox directory."""
        return self.root / self.inbox_dir

    @property
    def daily_notes(self) -> Path:
        """Full path to daily notes directory."""
        return self.root / self.daily_dir

    @property
    def weekly_notes(self) -> Path:
        """Full path to weekly notes directory."""
        return self.root / self.weekly_dir

    @property
    def daily_template_path(self) -> Path:
        """Full path to daily template."""
        return self.root / self.daily_template

    @property
    def weekly_template_path(self) -> Path:
        """Full path to weekly template."""
        return self.root / self.weekly_template


@dataclass(frozen=True)
class Config:
    """Main configuration container."""

    paths: PathConfig
    editor: EditorConfig

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment variables."""
        root_str = _get_env_required("ZETTELKASTEN")
        root = Path(root_str).expanduser().resolve()

        if not root.exists():
            raise ConfigurationError(
                f"Zettelkasten root directory does not exist: {root}"
            )

        return cls(
            paths=PathConfig(root=root),
            editor=EditorConfig(),
        )


# Lazy-loaded singleton
_config: Config | None = None


def get_config() -> Config:
    """Get the configuration singleton (lazy-loaded)."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config
