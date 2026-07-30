import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import recall_score, precision_score, f1_score
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, SLATE, style_figure


eyebrow("Section 4")
st.title("Can we fix the over-flagging with a stricter cutoff?")
st.markdown(
    """
The model classifies a restaurant as "Fail" whenever its predicted probability exceeds a cutoff,
0.5 by default. Because the models are trained with balanced class weights, they tend to
over-predict Fail. Raising the cutoff trades away some recall for fewer false positives citywide.
Adjust the threshold below to observe that tradeoff, and note its effect on the *gap* between the
least- and most-flagged neighborhoods.
"""
)

test = load_parquet("test_predictions.parquet")
require(test, "test_predictions.parquet")

y = test["y_true"].values
proba = test["proba_rf"].values
zips = test["Zip"].astype(str).values


def fpr_fn(yt, yp):
    neg = yt == 0
    return (yp[neg] == 1).mean() if neg.sum() else float("nan")


threshold = st.slider("Decision threshold", 0.30, 0.80, 0.50, 0.01)

pred = (proba >= threshold).astype(int)
recall = recall_score(y, pred, zero_division=0)
precision = precision_score(y, pred, zero_division=0)
fpr = fpr_fn(y, pred)
f1 = f1_score(y, pred, zero_division=0)

c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_card(f"{recall:.1%}", "recall (true failures caught)")
with c2:
    stat_card(f"{precision:.1%}", "precision")
with c3:
    stat_card(f"{fpr:.1%}", "false-positive rate", flag=True)
with c4:
    stat_card(f"{f1:.3f}", "F1")
st.caption("These four metrics recompute live as you move the threshold above.")

# --- per-ZIP FPR at this threshold ---
df = pd.DataFrame({"Zip": zips, "y": y, "pred": pred})
counts = df["Zip"].value_counts()
keep = counts[counts >= 100].index
passed = df[df["y"] == 0]
zip_fpr = passed[passed["Zip"].isin(keep)].groupby("Zip")["pred"].mean()

if len(zip_fpr) >= 10:
    lo = zip_fpr.quantile(0.10)
    hi = zip_fpr.quantile(0.90)
    ratio = (hi / lo) if lo > 0 else float("inf")
else:
    ratio = float("nan")

# guard the display: an unbounded gap (lo == 0) reads as ">=50x", too few ZIPs as "n/a"
if np.isfinite(ratio):
    ratio_txt = f"{ratio:.1f}×"
elif len(zip_fpr) >= 10:
    ratio_txt = "≥ 50×"
else:
    ratio_txt = "n/a"

st.divider()
eyebrow("The tradeoff that matters most")
c1, c2 = st.columns(2)
with c1:
    stat_card(f"{zip_fpr.min():.1%} \u2013 {zip_fpr.max():.1%}", "per-ZIP false-positive rate range")
with c2:
    stat_card(ratio_txt, "top-vs-bottom decile ZIP ratio (higher = wider gap)", flag=True)

st.markdown(
    """
Raise the threshold from **0.50 toward 0.60**. Citywide false positives fall substantially, but
the top-versus-bottom-decile ratio *increases* rather than decreases. At the thresholds tested in
the notebook:
"""
)

sweep = load_csv("threshold_sweep.csv")
if sweep is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["recall"], name="Recall",
                              line=dict(color=RED, width=2),
                              hovertemplate="Recall: %{y:.1%}<extra></extra>"))
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["precision"], name="Precision",
                              line=dict(color=BLUE, width=2),
                              hovertemplate="Precision: %{y:.1%}<extra></extra>"))
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["fpr"], name="FPR",
                              line=dict(color=SLATE, width=2, dash="dot"),
                              hovertemplate="FPR: %{y:.1%}<extra></extra>"))
    fig.add_vline(x=threshold, line_dash="dash", line_color=INK,
                  annotation_text="your cutoff", annotation_position="top",
                  annotation_font=dict(family="Space Mono, monospace", size=11, color=INK))
    style_figure(
        fig,
        xaxis_title="Threshold", yaxis_title="Rate", yaxis_tickformat=".0%",
        height=380, hovermode="x unified",
        legend=dict(orientation="h", y=1.1, font=dict(color=INK)),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    from utils import missing_file_notice
    missing_file_notice("threshold_sweep.csv")

finding(
    "Raising the threshold from 0.50 to 0.60 reduces citywide FPR from 44.5% to 16.2%, a large "
    "aggregate improvement. The per-ZIP top-versus-bottom-decile ratio, however, <b>widens from 5.4\u00d7 "
    "to 21.8\u00d7</b>. Tightening the cutoff improves the model in aggregate while"
    " widening the gap between neighborhoods: low-FPR ZIPs improve further while"
    " high-FPR ZIPs change little. A single global threshold cannot correct a disparity that operates"
    " at the ZIP level."
)

from utils import page_nav
page_nav(prev=("pages/3_Neighborhood_Effect.py", "Neighborhood Effect"), next=("pages/5_Fairness_Audit.py", "Fairness Audit"))
