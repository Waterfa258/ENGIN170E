# AI OCR Handoff

## What is included

- Gemini / Google AI Studio provider integrated into the existing backend gateway
- Prompt 1.1 and structured Pydantic output
- 17 label images under `images/raw/`
- Five-image reviewed ground truth and v1 result table
- Batch evaluator that regenerates 	est_results_v1.csv and ailure_log.md`n- Real Gemini 3.5 Flash result: 5/5 images fully matched, 15/15 target fields correct
- Automated verification: 46/46 backend unit tests passing

## Safe API-key setup

Do not paste an API key into chat or commit it to Git. In PowerShell, set it only for the current terminal:

```powershell
$env:GEMINI_API_KEY = "your-key"
$env:LABMIND_VISION_MODE = "live"
$env:LABMIND_PROVIDER = "gemini"
```

Alternatively copy `.env.example` to the Git-ignored `.env.local` and fill in `GEMINI_API_KEY`.

## Install and run

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python tools/evaluate_ocr.py --provider gemini --mode live --limit 5
```

The verified external run is saved as evaluation/test_results_gemini.csv and evaluation/failure_log_gemini.md. Use explicit --output and --failure-log paths when rerunning so the reviewed manual baseline is preserved.

## Integration contract

The UI and pipeline continue calling `backend.pipeline.analyze_label(...)`. Set `provider="gemini"` and `mode="live"`, or configure the equivalent environment variables. The response remains the same `OCRResult` / `AnalysisResult` schema used by the CS backend.
