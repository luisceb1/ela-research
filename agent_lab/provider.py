"""Minimal Responses API adapter. Explicit opt-in; never stores responses at the provider."""
from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


class ProviderError(RuntimeError):
    pass


class OpenAIProvider:
    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.model = model or os.environ.get("ELA_LAB_MODEL", "gpt-5-mini")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError("OPENAI_API_KEY is required for --live; --preview is free of model calls")

    def run(self, role: str, instructions: str, payload: dict, schema: dict) -> dict:
        request = {
            "model": self.model,
            "instructions": instructions,
            "input": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "text": {"format": {
                "type": "json_schema", "name": role, "strict": True, "schema": schema,
            }},
            "max_output_tokens": 2400,
            "store": False,
        }
        req = Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(request, ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=120) as response:
                data = json.loads(response.read(1_000_001))
        except Exception as exc:
            # Never include HTTP response content or authorization material in logs.
            raise ProviderError(f"Model request failed for {role}: {type(exc).__name__}") from None

        if data.get("status") != "completed":
            raise ProviderError(f"Incomplete model response from {role}")
        parts = []
        for item in data.get("output", []):
            if item.get("type") != "message":
                continue
            for content in item.get("content", []):
                if content.get("type") == "refusal":
                    raise ProviderError(f"Model refused the {role} task")
                if content.get("type") == "output_text":
                    parts.append(content.get("text", ""))
        if not parts:
            raise ProviderError(f"No JSON text returned by {role}")
        try:
            result = json.loads("".join(parts))
        except (TypeError, ValueError):
            raise ProviderError(f"Invalid JSON returned by {role}") from None
        if not isinstance(result, dict):
            raise ProviderError(f"Invalid object returned by {role}")
        return result
