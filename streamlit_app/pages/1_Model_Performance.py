import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from utils import apply_theme, eyebrow, stat_card, finding, load_parquet, require, BLUE, RED, INK, SLATE, style_figure, label_heatmap_cells


eyebrow("Section 1")
st.title("Does the model actually work?")
st.markdown(
    "Three predictors, same test set: a **naive baseline** that always guesses \"Pass\", "
    "**Logistic Regression**, and **Random Forest**. We grade them on **recall** — of the "
    "restaurants that truly failed, how many did each model catch? — since missing a real "
    "food-safety problem is the costly mistake here."
)

test = load_parquet("test_predictions.parquet")
require(test, "test_predictions.parquet")

y = test["y_true"].values


def metrics_row(name, y_pred):
    r = recall_score(y, y_pred, zero_division=0)
    p = precision_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    return dict(model=name, recall=r, precision=p, f1=f1, tn=tn, fp=fp, fn=fn, tp=tp)


rows = [
    metrics_row("Naive baseline", pd.Series([0] * len(y))),
    metrics_row("Logistic Regression", (test["proba_logreg"] >= 0.5).astype(int)),
    metrics_row("Random Forest", (test["proba_rf"] >= 0.5).astype(int)),
]
mt = pd.DataFrame(rows)

st.divider()
eyebrow("Head-to-head at the default 0.5 cutoff")
st.subheader("Recall, precision, and F1")

cols = st.columns(3)
for col, r in zip(cols, rows):
    with col:
        st.markdown(f"**{r['model']}**")
        st.metric("Recall (caught real fails)", f"{r['recall']:.1%}")
        st.metric("Precision (flags that were real)", f"{r['precision']:.1%}")
        st.metric("F1", f"{r['f1']:.3f}")

fig = px.bar(
    mt.melt(id_vars="model", value_vars=["recall", "precision", "f1"], var_name="metric", value_name="score"),
    x="model", y="score", color="metric", barmode="group",
    color_discrete_map={"recall": RED, "precision": BLUE, "f1": SLATE},
    height=380,
)
style_figure(fig, yaxis_tickformat=".0%", height=380)
st.plotly_chart(fig, use_container_width=True)

finding(
    "Both real models jump from <b>0% recall</b> (the naive baseline) to roughly "
    "<b>67&ndash;70%</b> — clear evidence the four features carry real signal. Logistic "
    "Regression edges out Random Forest on recall (69.8% vs 66.9%), which is a bit "
    "surprising given Random Forest is usually the stronger model of the two."
)

st.divider()
eyebrow("The cost side")
st.subheader("Confusion matrices")
st.caption("TN = correctly cleared,  FP = false alarm,  FN = missed a real fail,  TP = correctly flagged")

cols = st.columns(3)
for col, r in zip(cols, rows):
    with col:
        z = [[r["tn"], r["fp"]], [r["fn"], r["tp"]]]
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=["Pred: Pass", "Pred: Fail"],
            y=["True: Pass", "True: Fail"],
            colorscale=[[0, "#FFFFFF"], [1, RED]],
            showscale=False,
        ))
        label_heatmap_cells(fig, z)
        style_figure(fig, title=r["model"], height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

finding(
    "Precision sits around <b>30%</b> for both real models — about 7 in 10 flagged "
    "restaurants turn out fine. That's a real operational cost, though not necessarily "
    "disqualifying: missing a genuine hazard is usually worse than an extra inspection visit."
)

st.divider()
eyebrow("Is the model's confidence trustworthy?")
st.subheader("Calibration: what the model says vs. what actually happens")

from utils import load_csv
cal = load_csv("calibration_curve.csv")

if cal is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Perfectly calibrated",
                              line=dict(color=SLATE, dash="dash")))
    fig.add_trace(go.Scatter(x=cal["predicted"], y=cal["actual"], mode="lines+markers",
                              name="Random Forest", line=dict(color=RED, width=3)))
    style_figure(
        fig,
        xaxis_title="Predicted probability of Fail",
        yaxis_title="Actual fraction that failed",
        xaxis_tickformat=".0%", yaxis_tickformat=".0%",
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    finding(
        "The model is <b>overconfident</b>: when it says a restaurant has an 83% chance of "
        "failing, only about 43% actually do. Log loss confirms this &mdash; both trained "
        "models score <i>worse</i> than a naive constant-probability baseline (0.658 and "
        "0.701 vs. 0.533), meaning their confidence scores shouldn't be read at face value "
        "even though their yes/no calls beat the baseline. Read Fail/Pass predictions here "
        "as a ranked prioritization signal, not a calibrated risk percentage."
    )
else:
    from utils import missing_file_notice
    missing_file_notice("calibration_curve.csv")

from utils import page_nav
page_nav(prev=("home.py", "Overview"), next=("pages/2_What_Drives_Predictions.py", "What Drives Predictions"))
