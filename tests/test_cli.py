"""Basic tests for zettelkasten-cli."""


def test_import():
    """Test that the main module can be imported."""
    from zettelkasten_cli import main

    assert main.app is not None
