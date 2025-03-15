# To build the project

1. Make sure the `pyproject.toml` is present in the root directory.
2. Add if not present:

```toml
[tool.poetry.scripts]
zk = "zettelkasten_cli.main:app"
```

3. Run `poetry build`. This will create the wheel file in the `dist/` directory.

4. Next, `pipx install dist/zettelkasten_cli-0.1.0-py3-none-any.whl`

5. Finally, create a symlink to the `zk` command in your path: `ln -s ~/.local/share/pipx/venvs/zettelkasten-cli/bin/zk ~/.local/bin/`

Run `zk` to get started.
