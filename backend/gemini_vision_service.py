"""Google AI Studio / Gemini implementation of reagent-label extraction."""

from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any

from .schemas import OCRResult
from .vision_service import (
    LabelExtraction,
    SYSTEM_PROMPT,
    USER_PROMPT,
    _failed,
    _parse_live_response,
    _validate_image_path,
)


def _create_client(api_key: str) -> Any:
    try:
        from google import genai
    except ImportError as error:
        raise RuntimeError(
            "The google-genai package is not installed. Install requirements.txt."
        ) from error
    return genai.Client(api_key=api_key)


def _response_to_extraction(response: Any) -> LabelExtraction:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, LabelExtraction):
        return parsed
    if isinstance(parsed, dict):
        return LabelExtraction.model_validate(parsed)

    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Gemini returned no structured result.")
    return LabelExtraction.model_validate(json.loads(text))


def extract_label_with_gemini(
    image_path: str | Path,
    *,
    api_key: str,
    model: str,
    client: Any | None = None,
) -> OCRResult:
    """Extract a reagent label with Gemini structured JSON output."""

    try:
        path = _validate_image_path(image_path)
        active_client = client or _create_client(api_key)

        try:
            from google.genai import types
        except ImportError as error:
            raise RuntimeError(
                "The google-genai package is not installed. Install requirements.txt."
            ) from error

        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        response = active_client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type),
                f"{SYSTEM_PROMPT}\n\n{USER_PROMPT}",
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LabelExtraction,
                temperature=0,
            ),
        )
        return _parse_live_response(_response_to_extraction(response))
    except Exception as error:
        return _failed(f"Gemini Vision request failed ({type(error).__name__}).")
