import argparse
import json
import sys
from typing import Any, Dict, Optional

from .orchestrator import Orchestrator


def _print(obj: Any) -> None:
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="agi-protei", description="AGI Protei multi-plugin orchestrator")
    parser.add_argument("command", choices=["list-plugins", "invoke"], help="Command to run")
    parser.add_argument("--config", dest="config", default=None, help="Path to YAML config")

    # Common invoke options
    parser.add_argument("--tool", dest="tool", default=None, help="Tool name for invoke")
    parser.add_argument("--params", dest="params", default=None, help="Raw JSON params for invoke")

    # Convenience flags for common tools
    parser.add_argument("--text", dest="text", default=None, help="Text for echo")
    parser.add_argument("--a", dest="a", type=float, default=None, help="Operand A for math.add")
    parser.add_argument("--b", dest="b", type=float, default=None, help="Operand B for math.add")

    args = parser.parse_args(argv)

    orch = Orchestrator(config_path=args.config)
    orch.start()

    try:
        if args.command == "list-plugins":
            metas = orch.list_plugins()
            _print([m.__dict__ for m in metas])
            return 0
        elif args.command == "invoke":
            if not args.tool:
                parser.error("--tool is required for invoke")
            params: Dict[str, Any]
            if args.params:
                params = json.loads(args.params)
            else:
                params = {}
                if args.tool == "echo" and args.text is not None:
                    params = {"text": args.text}
                if args.tool == "math.add" and args.a is not None and args.b is not None:
                    params = {"a": args.a, "b": args.b}
            result = orch.invoke(args.tool, params)
            _print({"result": result})
            return 0
        else:
            parser.error("Unknown command")
    finally:
        orch.stop()


if __name__ == "__main__":
    raise SystemExit(main())
