import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from backend.gemini_vision_service import _response_to_extraction
from backend.provider_config import resolve_provider_config
from backend.schemas import ResultStatus
from backend.vision_gateway import extract_label_with_provider


class GeminiProviderTests(unittest.TestCase):
    def test_google_api_key_has_documented_precedence(self) -> None:
        config = resolve_provider_config(
            "gemini",
            environ={
                "GEMINI_API_KEY": "gemini-key",
                "GOOGLE_API_KEY": "google-key",
                "GEMINI_MODEL": "test-model",
            },
            env_path=None,
        )

        self.assertEqual(config.name, "gemini")
        self.assertEqual(config.api_key, "google-key")
        self.assertEqual(config.model, "test-model")

    def test_missing_key_returns_a_structured_failure(self) -> None:
        handle = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        handle.write(b"non-empty")
        handle.close()
        image_path = Path(handle.name)
        try:
            result = extract_label_with_provider(
                image_path,
                mode="live",
                provider="gemini",
                environ={},
                env_path=None,
            )
        finally:
            image_path.unlink(missing_ok=True)

        self.assertEqual(result.status, ResultStatus.FAILED)
        self.assertIn("GEMINI_API_KEY", result.error_message)

    def test_dict_structured_response_is_validated(self) -> None:
        response = SimpleNamespace(
            parsed={
                "catalog_number": "270741-2L",
                "lot_number": "SHBJ3763",
                "expiry_date": None,
                "brand": "Sigma-Aldrich",
                "product_name": "Reagent Alcohol for HPLC",
                "confidence": 0.99,
            }
        )

        parsed = _response_to_extraction(response)

        self.assertEqual(parsed.catalog_number, "270741-2L")
        self.assertEqual(parsed.lot_number, "SHBJ3763")


if __name__ == "__main__":
    unittest.main()
