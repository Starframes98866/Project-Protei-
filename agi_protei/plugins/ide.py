#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


META = {
    "name": "ide-ops",
    "version": "0.1.0",
    "language": "python",
    "capabilities": [
        "ide.list",
        "ide.read",
        "ide.write",
        "ide.search",
    ],
}


def _resolve_root(root: Optional[str]) -> str:
    root_dir = root or "/workspace"
    return os.path.abspath(root_dir)


def _resolve_path(root_abs: str, path: str) -> str:
    candidate = path
    if not os.path.isabs(candidate):
        candidate = os.path.join(root_abs, candidate)
    candidate_abs = os.path.abspath(candidate)
    # Enforce confinement to root
    if candidate_abs != root_abs and not candidate_abs.startswith(root_abs + os.sep):
        raise ValueError("Path escapes root")
    return candidate_abs


def _list_dir(root: Optional[str], path: str = ".", max_entries: int = 5000) -> Dict[str, Any]:
    root_abs = _resolve_root(root)
    dir_abs = _resolve_path(root_abs, path)
    if not os.path.isdir(dir_abs):
        raise ValueError("Not a directory")
    entries: List[Dict[str, Any]] = []
    for name in sorted(os.listdir(dir_abs)):
        full = os.path.join(dir_abs, name)
        try:
            st = os.stat(full)
        except Exception:
            continue
        entries.append({
            "name": name,
            "is_dir": os.path.isdir(full),
            "size": int(getattr(st, "st_size", 0)),
        })
        if len(entries) >= max_entries:
            break
    rel = os.path.relpath(dir_abs, root_abs)
    if rel == ".":
        rel = "/"
    return {"root": root_abs, "path": rel, "entries": entries}


def _read_file(root: Optional[str], path: str, max_bytes: int = 200_000, encoding: str = "utf-8") -> Dict[str, Any]:
    root_abs = _resolve_root(root)
    file_abs = _resolve_path(root_abs, path)
    if not os.path.isfile(file_abs):
        raise ValueError("Not a file")
    with open(file_abs, "rb") as f:
        data = f.read(max_bytes)
    try:
        text = data.decode(encoding, errors="replace")
        mode = "text"
        content: Any = text
    except Exception:
        mode = "bytes"
        content = list(data)
    rel = os.path.relpath(file_abs, root_abs)
    return {"root": root_abs, "path": rel, "mode": mode, "content": content}


def _write_file(root: Optional[str], path: str, content: str, encoding: str = "utf-8", create_dirs: bool = True) -> Dict[str, Any]:
    root_abs = _resolve_root(root)
    file_abs = _resolve_path(root_abs, path)
    parent = os.path.dirname(file_abs)
    if create_dirs and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    with open(file_abs, "w", encoding=encoding) as f:
        f.write(content)
    return {"root": root_abs, "path": os.path.relpath(file_abs, root_abs), "written_bytes": len(content.encode(encoding))}


def _search(root: Optional[str], path: str = ".", pattern: str = "", regex: bool = False, ignore_case: bool = True, max_matches: int = 2000) -> Dict[str, Any]:
    root_abs = _resolve_root(root)
    start_abs = _resolve_path(root_abs, path)
    if not os.path.isdir(start_abs):
        raise ValueError("Search path must be a directory")
    flags = re.IGNORECASE if ignore_case else 0
    matcher: Any
    if regex:
        matcher = re.compile(pattern, flags)
        def is_match(line: str) -> Optional[Tuple[int, int]]:
            m = matcher.search(line)
            return (m.start(), m.end()) if m else None
    else:
        needle = pattern.lower() if ignore_case else pattern
        def is_match(line: str) -> Optional[Tuple[int, int]]:
            hay = line.lower() if ignore_case else line
            i = hay.find(needle)
            if i == -1:
                return None
            return (i, i + len(pattern))

    results: List[Dict[str, Any]] = []
    for dirpath, dirnames, filenames in os.walk(start_abs):
        # Skip obvious noisy dirs
        base = os.path.basename(dirpath)
        if base in {".git", "node_modules", "venv", ".venv", "__pycache__"}:
            dirnames[:] = []
            continue
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root_abs)
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    for idx, line in enumerate(f, start=1):
                        span = is_match(line)
                        if span:
                            s, e = span
                            results.append({
                                "file": rel,
                                "line": idx,
                                "start": s,
                                "end": e,
                                "preview": line.rstrip("\n")
                            })
                            if len(results) >= max_matches:
                                return {"root": root_abs, "path": os.path.relpath(start_abs, root_abs), "pattern": pattern, "matches": results}
            except Exception:
                continue
    return {"root": root_abs, "path": os.path.relpath(start_abs, root_abs), "pattern": pattern, "matches": results}


def handle_invoke(tool: str, args: Dict[str, Any]) -> Any:
    if tool == "ide.list":
        return _list_dir(args.get("root"), args.get("path", "."), int(args.get("max_entries", 5000)))
    if tool == "ide.read":
        if not args.get("path"):
            raise ValueError("'path' is required")
        return _read_file(args.get("root"), args.get("path"), int(args.get("max_bytes", 200_000)), args.get("encoding", "utf-8"))
    if tool == "ide.write":
        if not args.get("path"):
            raise ValueError("'path' is required")
        return _write_file(args.get("root"), args.get("path"), str(args.get("content", "")), args.get("encoding", "utf-8"), bool(args.get("create_dirs", True)))
    if tool == "ide.search":
        return _search(
            args.get("root"),
            args.get("path", "."),
            str(args.get("pattern", "")),
            bool(args.get("regex", False)),
            bool(args.get("ignore_case", True)),
            int(args.get("max_matches", 2000)),
        )
    raise ValueError(f"Unknown tool: {tool}")


def serve() -> int:
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
                result = META
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


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args(argv)
    if args.serve:
        return serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
