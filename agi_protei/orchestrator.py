import json
import os
import sys
import subprocess
from typing import Any, Dict, List, Optional

from .plugin_protocol import PluginMeta


class ProcessJsonRpcClient:
    def __init__(self, command: List[str], plugin_id: str):
        self.command = command
        self.plugin_id = plugin_id
        self.process: Optional[subprocess.Popen] = None
        self._next_id = 1

    def start(self) -> None:
        if self.process is not None:
            return
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if self.process is None or self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("Process not started or missing pipes")
        request_id = self._next_id
        self._next_id += 1
        request_obj = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}
        line = json.dumps(request_obj) + "\n"
        self.process.stdin.write(line)
        self.process.stdin.flush()
        # Read responses until matching id
        while True:
            response_line = self.process.stdout.readline()
            if not response_line:
                raise RuntimeError(f"Plugin {self.plugin_id} terminated unexpectedly")
            try:
                response_obj = json.loads(response_line)
            except json.JSONDecodeError:
                # Ignore non-JSON lines
                continue
            if response_obj.get("id") == request_id:
                if "error" in response_obj and response_obj["error"]:
                    raise RuntimeError(f"Plugin error: {response_obj['error']}")
                return response_obj.get("result")

    def get_meta(self) -> PluginMeta:
        meta = self._send_request("get_meta")
        return PluginMeta(
            name=meta.get("name", self.plugin_id),
            version=meta.get("version", "0.0.0"),
            language=meta.get("language", "unknown"),
            capabilities=list(meta.get("capabilities", [])),
        )

    def invoke(self, tool: str, args: Dict[str, Any]) -> Any:
        return self._send_request("invoke", {"tool": tool, "args": args})

    def stop(self) -> None:
        if self.process is not None:
            try:
                if self.process.stdin:
                    try:
                        # Best-effort shutdown
                        self._send_request("shutdown")
                    except Exception:
                        pass
                self.process.terminate()
            finally:
                self.process = None


class Orchestrator:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.clients: Dict[str, ProcessJsonRpcClient] = {}
        self.metas: Dict[str, PluginMeta] = {}

    def _resolve_builtin_pytools_command(self) -> List[str]:
        package_dir = os.path.dirname(__file__)
        script_path = os.path.join(package_dir, "plugins", "pytools.py")
        return [sys.executable, script_path, "--serve"]

    def _load_config(self) -> List[Dict[str, Any]]:
        if not self.config_path:
            # Default to builtin Python tools only
            return [
                {"id": "pytools", "kind": "builtin_pytools"},
            ]
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "PyYAML is required to load YAML configs. Install 'pyyaml' or omit config_path."
            ) from exc
        with open(self.config_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        plugins = doc.get("plugins", []) if isinstance(doc, dict) else []
        return plugins

    def start(self) -> None:
        plugins = self._load_config()
        for p in plugins:
            plugin_id = p.get("id")
            kind = p.get("kind")
            optional = bool(p.get("optional", False))
            command: Optional[List[str]] = None
            if kind == "builtin_pytools":
                command = self._resolve_builtin_pytools_command()
            elif kind == "process":
                command = list(p.get("command", []))
            else:
                if optional:
                    continue
                raise ValueError(f"Unknown plugin kind: {kind}")

            if not command:
                if optional:
                    continue
                raise ValueError(f"No command resolved for plugin {plugin_id}")

            client = ProcessJsonRpcClient(command=command, plugin_id=plugin_id)
            try:
                client.start()
                meta = client.get_meta()
            except Exception as exc:
                if optional:
                    # Skip failing optional plugins
                    continue
                raise
            self.clients[plugin_id] = client
            self.metas[plugin_id] = meta

    def list_plugins(self) -> List[PluginMeta]:
        return list(self.metas.values())

    def invoke(self, tool: str, args: Dict[str, Any]) -> Any:
        # Route to first plugin that declares capability
        for plugin_id, meta in self.metas.items():
            if tool in meta.capabilities:
                client = self.clients[plugin_id]
                return client.invoke(tool, args)
        raise ValueError(f"No plugin found that supports tool '{tool}'")

    def stop(self) -> None:
        for client in self.clients.values():
            client.stop()
        self.clients.clear()
        self.metas.clear()
