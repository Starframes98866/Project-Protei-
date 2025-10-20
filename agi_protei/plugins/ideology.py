#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List


META = {
    "name": "ideology",
    "version": "0.1.0",
    "language": "python",
    "capabilities": [
        "ideology.info",
        "ideology.compare",
    ],
}

# Neutral, high-level summaries intended for informational use only.
SUMMARIES: Dict[str, Dict[str, Any]] = {
    "communism": {
        "summary": (
            "Communism is a socio-economic ideology and movement advocating for a classless, "
            "stateless society featuring common ownership of the means of production and production for use."
        ),
        "core_principles": [
            "Common ownership of productive assets",
            "Abolition of class distinctions",
            "Allocation based on needs rather than market exchange",
        ],
    },
    "socialism": {
        "summary": (
            "Socialism generally refers to systems where the means of production are collectively or publicly owned, "
            "with varying degrees of market mechanisms and planning across different models."
        ),
        "core_principles": [
            "Collective or public ownership of major industries",
            "Economic coordination through planning or regulated markets",
            "Greater emphasis on social welfare and equity",
        ],
    },
    "capitalism": {
        "summary": (
            "Capitalism is an economic system characterized by private ownership of the means of production, "
            "market-based allocation of goods and services, and profit-driven enterprise."
        ),
        "core_principles": [
            "Private property and capital accumulation",
            "Voluntary exchange via markets",
            "Competition and price signals for resource allocation",
        ],
    },
}


def info(topic: str) -> Dict[str, Any]:
    key = topic.strip().lower()
    data = SUMMARIES.get(key)
    if not data:
        return {
            "topic": topic,
            "summary": "No summary available.",
            "core_principles": [],
        }
    return {
        "topic": key,
        **data,
    }


def compare(a: str, b: str) -> Dict[str, Any]:
    ia = info(a)
    ib = info(b)
    similarities: List[str] = []
    differences: List[str] = []

    # Very simple, neutral comparison logic
    if ia["topic"] == "communism" and ib["topic"] == "socialism" or ia["topic"] == "socialism" and ib["topic"] == "communism":
        similarities.append("Both emphasize collective approaches over purely private ownership.")
        differences.append("Communism typically envisions a stateless, classless end-state; socialism spans diverse models.")
    if ia["topic"] == "capitalism" and ib["topic"] in ("socialism", "communism") or ib["topic"] == "capitalism" and ia["topic"] in ("socialism", "communism"):
        similarities.append("All are frameworks addressing production, ownership, and distribution.")
        differences.append("Capitalism centers private ownership and markets; the others increase or prioritize collective ownership.")

    return {
        "a": ia,
        "b": ib,
        "similarities": similarities,
        "differences": differences,
        "disclaimer": (
            "This is a brief, neutral summary for informational purposes; consult primary sources for depth."
        ),
    }


def handle_invoke(tool: str, args: Dict[str, Any]) -> Any:
    if tool == "ideology.info":
        topic = str(args.get("topic", "")).strip()
        if not topic:
            raise ValueError("'topic' is required")
        return info(topic)
    if tool == "ideology.compare":
        a = str(args.get("a", "")).strip()
        b = str(args.get("b", "")).strip()
        if not a or not b:
            raise ValueError("'a' and 'b' are required")
        return compare(a, b)
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args(argv)
    if args.serve:
        return serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
