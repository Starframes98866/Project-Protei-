from dataclasses import dataclass
from typing import Any, Dict, List, Optional

JSONDict = Dict[str, Any]


@dataclass
class PluginMeta:
    name: str
    version: str
    language: str
    capabilities: List[str]


@dataclass
class RpcRequest:
    jsonrpc: str
    id: int
    method: str
    params: Optional[JSONDict]


@dataclass
class RpcResponse:
    jsonrpc: str
    id: int
    result: Optional[Any]
    error: Optional[JSONDict]
