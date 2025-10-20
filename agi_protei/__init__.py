"""AGI Protei Python SDK (experimental).

Exports the top-level `Protei` client and plugin primitives.
"""
from .client import Protei
from .plugins import Plugin, PluginManager
from .modules import IdeologicalCommunistModule, IDEModule, GameDevModule, SpaceModule

__all__ = [
    "Protei",
    "Plugin",
    "PluginManager",
    "IdeologicalCommunistModule",
    "IDEModule",
    "GameDevModule",
    "SpaceModule",
]
