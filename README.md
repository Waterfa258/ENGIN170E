# LabMind Backend

## Our Task

Our part builds the vision API and backend pipeline that converts a reagent-label image into structured OCR data, inventory and expiry results, and alternative recommendations for the Streamlit UI.

## How to Run

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
```

Create and activate a virtual environment, install the dependencies, and create the local configuration in Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

The default configuration uses mock mode, so it does not make a billable API request. Run the backend with any non-empty `.jpg`, `.jpeg`, `.png`, or `.webp` image:

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

Run the automated tests with:

```bash
python -m unittest discover -s tests
```

For live OCR, change `LABMIND_VISION_MODE` to `live` in `.env.local` and add the appropriate provider API key. Never commit `.env.local`.

## Current Progress

- The backend MVP is complete, including structured OCR, provider configuration, inventory lookup, expiry warnings, product enrichment, and alternative recommendations.
- The sample data currently contains 20 products, 20 inventory records, and 6 alternative mappings.
- All 43 automated backend tests are passing.
- The remaining work is Streamlit UI integration, OCR prompt evaluation with real label images, and end-to-end team testing.
