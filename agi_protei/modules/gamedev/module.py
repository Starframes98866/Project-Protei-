from __future__ import annotations

from typing import Any, Dict, List, Optional

from ...plugins import Plugin


class GameDevModule(Plugin):
    """Utilities focused on game development prompts/responses.

    - Highlights TODOs and bug tickets in responses
    - Annotates prompts with a concise game-dev context block when provided
    - Can extract bullet lists of tasks from a response for tracking
    """

    name = "gamedev"

    def on_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        if not prompt:
            return prompt
        game_context: Optional[Dict[str, Any]] = context.get("gamedev") if isinstance(context, dict) else None
        if not game_context:
            return prompt

        parts: List[str] = [prompt]
        title = game_context.get("title") or game_context.get("project")
        engine = game_context.get("engine")
        platform = game_context.get("platform")
        genre = game_context.get("genre")
        if title or engine or platform or genre:
            header_bits: List[str] = []
            if title:
                header_bits.append(f"Title: {title}")
            if engine:
                header_bits.append(f"Engine: {engine}")
            if platform:
                header_bits.append(f"Platform: {platform}")
            if genre:
                header_bits.append(f"Genre: {genre}")
            header = "; ".join(header_bits)
            parts.insert(0, f"[GameDev Context] {header}")
        return "\n".join(parts)

    def on_response(self, response: str, context: Dict[str, Any]) -> str:
        if not response:
            return response
        # Normalize TODO markers to a common style for downstream tooling
        normalized = response.replace("[ ]", "- [ ]").replace("[x]", "- [x]")
        return normalized
