# Chicago Food Inspections — Streamlit App

Interactive walkthrough of the Group 11D fairness audit: does ZIP code drive Chicago food
inspection failure predictions, and if so, does it track real risk or enforcement patterns?

## 1. Get your artifacts

Run the export cell at the end of the Colab notebook (`food_inspections.ipynb`). It writes a
`streamlit_artifacts/` folder to your Google Drive containing:

```
rf_with_zip.joblib
rf_no_zip.joblib
logreg.joblib
test_predictions.parquet
permutation_importance.csv
zip_flip_summary.csv
zip_fpr_fnr.csv 
zip_enforcement_compare.csv
threshold_sweep.csv
calibration_curve.csv
zip_centroids.csv
```

Download that folder from Drive, and copy its **contents** (not the folder itself) into this
project's `artifacts/` folder, so you end up with e.g. `artifacts/test_predictions.parquet`.

> Note: the app reads its numbers straight from the CSV/Parquet files — the `.joblib` model
> files aren't required to run the site itself, since all predictions were already exported.
> Keep them in the folder anyway in case you extend the app later (e.g. a live "score a new
> restaurant" form).

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run it

```bash
streamlit run app.py
```

It'll open at `http://localhost:8501`. The sidebar lists all seven sections in order.

## 4. Missing a file?

Each page will show a yellow notice naming the exact file it's missing and stop rendering
the rest of that page — the other pages will still work independently.

## Deploying

To share this publicly (e.g. via Streamlit Community Cloud), push this whole folder —
including populated `artifacts/` — to a GitHub repo, then point Streamlit Cloud at `app.py`.
The Parquet/CSV files are small enough to commit directly; no external database needed.
