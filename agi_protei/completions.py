from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Generator


@dataclass
class CompletionResult:
    model: str
    prompt: str
    text: str


class CompletionsClient:
    """Local, stubbed completions client with plugin stages.

    This class simulates a completion API so the examples in `docs/` run.
    """

    def __init__(self, owner) -> None:
        self._owner = owner

    def create(self, *, model: str, prompt: str, **_: Any) -> CompletionResult:
        context: Dict[str, Any] = {"model": model}
        prompt_transformed = self._owner.plugins.apply_on_prompt(prompt, context)

        # Placeholder inference: echo the prompt in a structured way
        raw = f"Echo (model={model}): {prompt_transformed}"

        text = self._owner.plugins.apply_on_response(raw, context)
        return CompletionResult(model=model, prompt=prompt_transformed, text=text)

    def stream(self, *, model: str, prompt: str, delay_ms: int = 30, **_: Any) -> Generator[str, None, None]:
        context: Dict[str, Any] = {"model": model}
        prompt_transformed = self._owner.plugins.apply_on_prompt(prompt, context)
        # Generate a fake stream from the transformed prompt
        raw = f"Echo (model={model}): {prompt_transformed}"
        # Apply post-processing after complete message, then stream chunks
        full = self._owner.plugins.apply_on_response(raw, context)
        for token in full.split():
            yield token + " "
            if delay_ms:
                time.sleep(delay_ms / 1000.0)
