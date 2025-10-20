from __future__ import annotations

import re
from typing import Any, Dict

from ...plugins import Plugin


class IDEModule(Plugin):
    """Simple IDE-flavored response utilities.

    - Ensures code fences are balanced
    - Optionally wraps likely code in fenced blocks (conservative)
    """

    name = "ide"

    _CODE_HINT = re.compile(r"\b(def |class |import |from |function |var |let |const |#include )")

    def on_response(self, response: str, context: Dict[str, Any]) -> str:
        if not response:
            return response

        balanced = self._ensure_balanced_fences(response)
        # Conservative: only wrap if the whole message looks like code and no fences exist
        if "```" not in balanced and self._looks_like_mostly_code(balanced):
            # Default to plaintext code block since language is unknown
            return f"```\n{balanced}\n```"
        return balanced

    def _ensure_balanced_fences(self, text: str) -> str:
        fence_count = text.count("```")
        if fence_count % 2 == 1:
            # Add a closing fence to balance
            return text + "\n```"
        return text

    def _looks_like_mostly_code(self, text: str) -> bool:
        # Heuristic: at least 3 lines with code-like tokens
        lines = [ln for ln in text.splitlines() if ln.strip()]
        matches = sum(1 for ln in lines if self._CODE_HINT.search(ln))
        return matches >= 3
