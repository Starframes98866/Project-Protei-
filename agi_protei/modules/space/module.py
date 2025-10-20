from __future__ import annotations

from typing import Any, Dict

from ...plugins import Plugin


class SpaceModule(Plugin):
    """Space/science domain guardrails and helpers.

    - Prefaces prompts to encourage unit clarity and sources
    - Post-processes responses to include unit reminders when numbers are present
    """

    name = "space"

    def on_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        if not prompt:
            return prompt
        preface = (
            "When discussing space or astrophysics, use clear SI units, cite known "
            "constants when relevant, and note assumptions. "
        )
        # Avoid double-prefacing if user already included an instruction
        return prompt if prompt.startswith("When discussing space or astrophysics") else f"{preface}{prompt}"

    def on_response(self, response: str, context: Dict[str, Any]) -> str:
        if not response:
            return response
        # If there are numeric values, remind about units unless already present
        has_digit = any(ch.isdigit() for ch in response)
        if has_digit and "km" not in response and "m/s" not in response and "kg" not in response:
            reminder = (
                "\nNote: Ensure all numeric quantities include units (e.g., km, m/s, kg)."
            )
            return response + reminder
        return response
