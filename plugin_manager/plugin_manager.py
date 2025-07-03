from pathlib import Path
from typing import Any


class PluginManager:
    def __init__(self, path: Path):
        self._path = path
        self._plugins: dict[str, type[Any]] = {}
        self._discover_plugins()

    def _discover_plugins(self) -> None:
        self._plugins.clear()
        for file in self._path.glob("*.py"):
            if file.stem in ("__init__", ):
                continue
            print(file)