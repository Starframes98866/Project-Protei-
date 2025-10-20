from __future__ import annotations

import re
from typing import Any, Dict

from ...plugins import Plugin


class IdeologicalCommunistModule(Plugin):
    """A neutrality-focused ideology guard.

    Despite the name, this module enforces a neutral, non-persuasive tone on
    political or ideological content. It avoids targeted persuasion and frames
    outputs as informational summaries.
    """

    name = "ideological-communist"

    _TARGETED_PERSUASION = re.compile(
        r"\b(convince|vote|support|campaign|donate|join|persuade|urge|should vote|" r"endorse|rally|party|elect)\b",
        re.IGNORECASE,
    )

    def on_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        # Preface prompts to enforce neutral, descriptive output
        neutral_preface = (
            "Please respond in a neutral, non-persuasive, factual tone. "
            "Avoid calls to action or targeted political advice. "
        )
        transformed = f"{neutral_preface}{prompt}" if not prompt.lower().startswith("please respond in a neutral") else prompt
        return transformed

    def on_response(self, response: str, context: Dict[str, Any]) -> str:
        # If the response appears to include calls to action, de-emphasize them
        if self._TARGETED_PERSUASION.search(response or ""):
            disclaimer = (
                "Note: The following information is presented neutrally and avoids "
                "persuasion or calls to action. "
            )
            return f"{disclaimer}{response}"
        return response
