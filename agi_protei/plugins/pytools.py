#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import asdict
from typing import Any, Dict


PLUGIN_META = {
    "name": "builtin-pytools",
    "version": "0.1.0",
    "language": "python",
    "capabilities": [
        "echo",
        "math.add",
    ],
}


def handle_invoke(tool: str, args: Dict[str, Any]) -> Any:
    if tool == "echo":
        return str(args.get("text", ""))
    if tool == "math.add":
        a = float(args.get("a", 0))
        b = float(args.get("b", 0))
        return a + b
    raise ValueError(f"Unknown tool: {tool}")


def serve() -> int:
    # Simple line-delimited JSON-RPC 2.0 server
    stdin = sys.stdin
    stdout = sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}
        try:
            if method == "get_meta":
                result = PLUGIN_META
            elif method == "invoke":
                tool = params.get("tool")
                args = params.get("args") or {}
                result = handle_invoke(tool, args)
            elif method == "shutdown":
                print(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": True}), file=stdout, flush=True)
                return 0
            else:
                raise ValueError("Unknown method")
            print(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}), file=stdout, flush=True)
        except Exception as exc:
            print(
                json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"message": str(exc)},
                }),
                file=stdout,
                flush=True,
            )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args(argv)
    if args.serve:
        return serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
