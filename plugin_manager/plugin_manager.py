import importlib.util
import inspect
from pathlib import Path
from types import FunctionType, ModuleType
from typing import Any


class PluginManager:
    def __init__(self, path: Path):
        self._path: Path = Path(path)
        if not (path.exists() and path.is_dir()):
            raise ValueError(f"Path '{self._path}' '{self._path.absolute()}' doesn't exist")
        self._plugins: dict[str, FunctionType] = {}
        self._discover_plugins()

    @staticmethod
    def load_module_from_path(file_path: Path) -> ModuleType:
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            raise ImportError(f"Cannot load module from {file_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def get_functions_from_file(file_path: Path) -> dict[str, FunctionType]:
        module = PluginManager.load_module_from_path(file_path)
        functions = {}
        for _, obj in inspect.getmembers(module, inspect.isfunction):
            mod = inspect.getmodule(obj)
            if mod is None or mod == module:  # only include functions from this file
                functions[module.__name__] = obj
        return functions

    def _discover_plugins(self) -> None:
        self._plugins.clear()
        for file in self._path.glob("*.py"):
            if file.stem in ("__init__",):
                continue
            functions: dict[str, FunctionType] = PluginManager.get_functions_from_file(file)
            self._plugins.update(functions)
            for name, fn in functions.items():
                print(f"Module: {name} | Signature: {inspect.signature(fn)}")

    @property
    def types(self) -> list[str]:
        return list(self._plugins.keys())

    def list(self) -> list[str]:
        return list(self._plugins.keys())

    def get(self, name: str) -> Any:
        if not self._plugins:
            raise KeyError("Plugins haven't been loaded yet")
        plugin_cls = self._plugins.get(name)
        if plugin_cls:
            return plugin_cls
        raise KeyError(f"Plugin '{name}' not found")
