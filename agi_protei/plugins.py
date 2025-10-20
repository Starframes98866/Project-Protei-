from __future__ import annotations

from abc import ABC
from typing import Any, Dict, List


class Plugin(ABC):
    """Base class for Protei plugins.

    Plugins can inspect and transform the prompt and the response.
    Implementors should be pure functions where possible to keep behavior predictable.
    """

    name: str = "plugin"

    def on_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        """Transform or annotate the prompt before it is sent to the model.

        Implementations should return the (possibly) modified prompt.
        """
        return prompt

    def on_response(self, response: str, context: Dict[str, Any]) -> str:
        """Transform or annotate the raw response prior to returning to callers."""
        return response

    def on_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """Optional error hook."""
        return None


class PluginManager:
    """Coordinates a sequence of plugins.

    Plugins are executed in registration order. Each stage receives and returns
    a string so transformations can be composed deterministically.
    """

    def __init__(self, plugins: List[Plugin] | None = None) -> None:
        self._plugins: List[Plugin] = list(plugins or [])

    @property
    def plugins(self) -> List[Plugin]:
        return list(self._plugins)

    def register(self, plugin: Plugin) -> None:
        self._plugins.append(plugin)

    def apply_on_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        transformed = prompt
        for plugin in self._plugins:
            try:
                transformed = plugin.on_prompt(transformed, context)
            except Exception as exc:  # keep plugins isolated
                try:
                    plugin.on_error(exc, context)
                finally:
                    # best-effort isolation: continue with previous transformed value
                    continue
        return transformed

    def apply_on_response(self, response: str, context: Dict[str, Any]) -> str:
        transformed = response
        for plugin in self._plugins:
            try:
                transformed = plugin.on_response(transformed, context)
            except Exception as exc:
                try:
                    plugin.on_error(exc, context)
                finally:
                    continue
        return transformed
