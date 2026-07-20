# OCR Failure Log v1

## Summary

- Images reviewed: 5
- Correctly transcribed visible catalog/lot/expiry fields: 5/5
- Images with a visible catalog number: 2/5
- Images missing a catalog number on the source label: 3/5
- Character-level OCR mistakes observed during manual AI review: 0

## Cases requiring pipeline handling

### label_01.png

- Visible: lot `7439`, expiry `09/17`
- Missing: catalog number
- Expected backend behavior: OCR may return partial fields; inventory matching must report that catalog lookup cannot run.

### label_02.png

- Visible: batch `AC45739`, expiry `10/2026`
- Missing: catalog number
- Expected backend behavior: do not invent a catalog number.

### label_03.png

- Visible: lot `0001234`, expiry `09/13/26`
- Missing: catalog number
- Expected backend behavior: preserve the leading zeros and do not invent a catalog number.

## Prompt 1.0 findings

The anti-hallucination instruction is important: three of the first five images genuinely do not contain a catalog number. A useful field-level OCR score must treat an expected blank matched by an output blank as correct, while the end-to-end inventory pipeline should separately mark those images as not matchable.

This v1 file records Codex manual visual review, not a billed external API run. Run `tools/evaluate_ocr.py` with `--provider gemini --mode live` after setting a local Gemini key to generate the automated benchmark.
