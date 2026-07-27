import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import recall_score, precision_score, f1_score
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, SLATE, style_figure

st.set_page_config(page_title="Threshold Tuning", page_icon="\U0001F37D\uFE0F", layout="wide")
apply_theme()

eyebrow("Section 4")
st.title("Can we fix the over-flagging with a stricter cutoff?")
st.markdown(
    """
The model flags "Fail" whenever its predicted probability crosses a cutoff — 0.5 by default.
Because the models are trained with balanced class weights, they lean toward over-predicting
Fail. Raising the cutoff trades away some recall for fewer false alarms citywide. Drag the
slider to see that tradeoff — and watch what it does to the *gap* between the least- and
most-flagged neighborhoods.
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


threshold = st.slider("Decision threshold", 0.20, 0.85, 0.50, 0.01)

pred = (proba >= threshold).astype(int)
recall = recall_score(y, pred, zero_division=0)
precision = precision_score(y, pred, zero_division=0)
fpr = fpr_fn(y, pred)
f1 = f1_score(y, pred, zero_division=0)

c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_card(f"{recall:.1%}", "recall (real fails caught)")
with c2:
    stat_card(f"{precision:.1%}", "precision")
with c3:
    stat_card(f"{fpr:.1%}", "false-positive rate", flag=True)
with c4:
    stat_card(f"{f1:.3f}", "F1")

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

st.divider()
eyebrow("The tradeoff that matters most")
c1, c2 = st.columns(2)
with c1:
    stat_card(f"{zip_fpr.min():.1%} \u2013 {zip_fpr.max():.1%}", "per-ZIP false-positive rate range")
with c2:
    stat_card(f"{ratio:.1f}\u00d7", "top-vs-bottom decile ZIP ratio (higher = wider gap)", flag=True)

st.markdown(
    """
Try dragging the slider from **0.50 up toward 0.60**. Citywide false alarms drop a lot — but
the top-vs-bottom-decile ratio *climbs*, not falls. At the notebook's tested thresholds:
"""
)

sweep = load_csv("threshold_sweep.csv")
if sweep is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["recall"], name="Recall",
                              line=dict(color=RED, width=2)))
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["precision"], name="Precision",
                              line=dict(color=BLUE, width=2)))
    fig.add_trace(go.Scatter(x=sweep["threshold"], y=sweep["fpr"], name="FPR",
                              line=dict(color=SLATE, width=2, dash="dot")))
    fig.add_vline(x=threshold, line_dash="dash", line_color=INK)
    style_figure(
        fig,
        xaxis_title="Threshold", yaxis_title="Rate", yaxis_tickformat=".0%",
        height=380,
        legend=dict(orientation="h", y=1.1, font=dict(color=INK)),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    from utils import missing_file_notice
    missing_file_notice("threshold_sweep.csv")

finding(
    "Raising the threshold from 0.50 to 0.60 cuts citywide FPR from 44.5% to 16.2% — a big "
    "improvement on paper. But the per-ZIP top-vs-bottom-decile ratio <b>widens from 5.4\u00d7 "
    "to 21.8\u00d7</b>. Tightening the cutoff makes the model look better in aggregate while "
    "making the gap between neighborhoods <i>worse</i> \u2014 low-FPR ZIPs improve further, "
    "high-FPR ZIPs barely move. A single global threshold can't fix a disparity that lives "
    "at the ZIP level."
)
