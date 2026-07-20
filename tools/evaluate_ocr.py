"""Batch-evaluate reagent-label OCR and write Checkpoint 1 artifacts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.date_utils import normalize_expiry_date
from backend.vision_gateway import extract_label_with_provider


FIELDS = ("catalog_number", "lot_number", "expiry_date")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def _clean(value: object) -> str:
    return "" if value is None else str(value).strip()


def _normalized(field: str, value: object) -> str:
    text = _clean(value)
    if field == "expiry_date":
        return normalize_expiry_date(text) or ""
    return text.upper()


def _load_truth(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["image_name"]: row for row in csv.DictReader(handle)}


def _match(field: str, expected: object, actual: object) -> bool:
    return _normalized(field, expected) == _normalized(field, actual)


def evaluate(args: argparse.Namespace) -> list[dict[str, object]]:
    truth = _load_truth(args.ground_truth)
    images = sorted(
        path
        for path in args.images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )[: args.limit]

    rows: list[dict[str, object]] = []
    for image_path in images:
        expected = truth.get(image_path.name, {})
        result = extract_label_with_provider(
            image_path,
            mode=args.mode,
            provider=args.provider,
        )
        actual = result.to_dict()
        matches = {
            field: _match(field, expected.get(field), actual.get(field))
            for field in FIELDS
        }
        rows.append(
            {
                "image_name": image_path.name,
                "provider": args.provider,
                "ocr_status": result.status.value,
                "expected_catalog_number": _clean(expected.get("catalog_number")),
                "expected_lot_number": _clean(expected.get("lot_number")),
                "expected_expiry_date": _normalized(
                    "expiry_date", expected.get("expiry_date")
                ),
                "ai_catalog_number": _clean(result.catalog_number),
                "ai_lot_number": _clean(result.lot_number),
                "ai_expiry_date": _clean(result.expiry_date),
                "catalog_match": matches["catalog_number"],
                "lot_match": matches["lot_number"],
                "expiry_match": matches["expiry_date"],
                "all_three_match": all(matches.values()),
                "confidence": result.confidence,
                "error_message": _clean(result.error_message),
            }
        )
    return rows


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit("No supported images were found.")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_failure_log(path: Path, rows: list[dict[str, object]]) -> None:
    failures = [
        row
        for row in rows
        if row["ocr_status"] != "success" or not row["all_three_match"]
    ]
    lines = [
        "# OCR Failure Log",
        "",
        f"- Images evaluated: {len(rows)}",
        f"- Fully matched: {len(rows) - len(failures)}",
        f"- Needs review: {len(failures)}",
        "",
    ]
    if not failures:
        lines.append("No failures in this run.")
    for row in failures:
        lines.extend(
            [
                f"## {row['image_name']}",
                "",
                f"- OCR status: {row['ocr_status']}",
                f"- Catalog match: {row['catalog_match']}",
                f"- Lot match: {row['lot_match']}",
                f"- Expiry match: {row['expiry_match']}",
                f"- Error: {row['error_message'] or 'field mismatch'}",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images-dir", type=Path, default=PROJECT_ROOT / "images" / "raw")
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=PROJECT_ROOT / "evaluation" / "ground_truth_v1.csv",
    )
    parser.add_argument("--provider", default="gemini")
    parser.add_argument("--mode", choices=("mock", "live"), default="live")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "evaluation" / "test_results_v1.csv",
    )
    parser.add_argument(
        "--failure-log",
        type=Path,
        default=PROJECT_ROOT / "evaluation" / "failure_log.md",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    evaluation_rows = evaluate(arguments)
    _write_csv(arguments.output, evaluation_rows)
    _write_failure_log(arguments.failure_log, evaluation_rows)
    print(f"Wrote {len(evaluation_rows)} rows to {arguments.output}")
