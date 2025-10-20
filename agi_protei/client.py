from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from .plugins import Plugin, PluginManager
from .completions import CompletionsClient


class Protei:
    """Top-level AGI Protei client.

    This minimal, local implementation provides a plugin pipeline and stubbed
    completion methods compatible with the documentation examples. It does not
    contact any remote service.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        plugins: Optional[List[Plugin]] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key: Optional[str] = api_key or os.getenv("PROTEI_API_KEY")
        self.base_url: Optional[str] = base_url or os.getenv("PROTEI_BASE_URL")
        self.plugins = PluginManager(plugins)
        self.completions = CompletionsClient(self)

    def with_plugins(self, plugins: List[Plugin]) -> "Protei":
        """Return a shallow copy with an extended plugin list."""
        new = Protei(api_key=self.api_key, base_url=self.base_url)
        for plugin in self.plugins.plugins + list(plugins):
            new.plugins.register(plugin)
        return new

    def add_plugin(self, plugin: Plugin) -> None:
        self.plugins.register(plugin)
