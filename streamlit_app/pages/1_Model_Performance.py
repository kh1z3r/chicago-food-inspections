import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from utils import apply_theme, eyebrow, stat_card, finding, load_parquet, require, BLUE, RED, INK, SLATE, style_figure, label_heatmap_cells


eyebrow("Section 1")
st.title("Does the model actually work?")
st.markdown(
    "Three predictors, evaluated on the same held-out test set: a **naive baseline** that always "
    "predicts \"Pass\", **Logistic Regression**, and **Random Forest**. The primary metric is "
    "**recall**, the fraction of truly failing restaurants each model correctly flagged. Recall is "
    "prioritized here because a missed failure (an uncaught food-safety hazard) is the costlier error."
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
eyebrow("Performance at the default 0.5 cutoff")
st.subheader("Recall, precision, and F1")

cols = st.columns(3)
for col, r in zip(cols, rows):
    with col:
        st.markdown(f"**{r['model']}**")
        st.metric("Recall (caught real fails)", f"{r['recall']:.1%}")
        st.metric("Precision (flags that were real)", f"{r['precision']:.1%}")
        st.metric("F1", f"{r['f1']:.3f}")

# recall and precision are rates, so they belong on the % axis; F1 is a 0-1 score shown in the cards above.
_melt = mt.melt(id_vars="model", value_vars=["recall", "precision"], var_name="metric", value_name="score")
_melt["metric"] = _melt["metric"].str.capitalize()
fig = px.bar(
    _melt, x="model", y="score", color="metric", barmode="group",
    color_discrete_map={"Recall": BLUE, "Precision": RED},
    labels={"model": "Model", "score": "Score", "metric": "Metric"}, height=380,
)
fig.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y:.1%}<extra></extra>")
fig.add_annotation(x="Naive baseline", y=0.015, text="0%", showarrow=False,
                   font=dict(family="Space Mono, monospace", size=12, color=INK))
style_figure(fig, yaxis_tickformat=".0%", height=380)
st.plotly_chart(fig, use_container_width=True)

finding(
    "Both trained models rise from <b>0% recall</b> (the naive baseline) to roughly "
    "<b>67% to 70%</b>, evidence that the four features carry real predictive signal. Logistic "
    "Regression slightly outperforms Random Forest on recall (69.8% versus 66.9%)."
)

st.divider()
eyebrow("The cost of false positives")
st.subheader("Confusion matrices")
st.caption("FN = missed fail (top left),  TP = correctly flagged fail (top right)  "
           "TN = correctly flagged pass (bottom left),  FP = missed pass (bottom right)")

cols = st.columns(3)
for col, r in zip(cols, rows):
    with col:
        z = [[r["tn"], r["fp"]], [r["fn"], r["tp"]]]
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=["Pred: Pass", "Pred: Fail"],
            y=["True: Pass", "True: Fail"],
            colorscale=[[0, "#FFFFFF"], [1, BLUE]],
            showscale=False, hoverinfo="skip",
        ))
        label_heatmap_cells(fig, z)
        style_figure(fig, title=r["model"], height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

finding(
    "Why predict failures over passes? We want to build our model around minimizing real failures."
    "We would rather overflag and verify a restaurant than underflag and miss a mistake."
    "This decision brings more importance towards recall rather than accuracy."
)

st.divider()
eyebrow("Is the model's confidence trustworthy?")
st.subheader("Calibration: predicted probability versus observed failure rate")

from utils import load_csv
cal = load_csv("calibration_curve.csv")

if cal is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Perfectly calibrated",
                              line=dict(color=SLATE, dash="dash"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=cal["predicted"], y=cal["actual"], mode="lines+markers",
                              name="Random Forest", line=dict(color=RED, width=3),
                              hovertemplate="Predicted %{x:.0%}<br>Actual %{y:.0%}<extra>Random Forest</extra>"))
    style_figure(
        fig,
        xaxis_title="Predicted probability of Fail",
        yaxis_title="Actual fraction that failed",
        xaxis_tickformat=".0%", yaxis_tickformat=".0%",
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    finding(
        "The model is <b>overconfident</b>: among restaurants it assigns an 83% probability of "
        "failing, only about 43% actually fail. Log loss confirms this. However, this in fact "
        "supports our decision where we are prioritizing overflagging errors, as we would rather " 
        "risk being wrong about failing, than being wrong about passing and letting a failing health restaurant continue operations."
    )
else:
    from utils import missing_file_notice
    missing_file_notice("calibration_curve.csv")

from utils import page_nav
page_nav(prev=("home.py", "Overview"), next=("pages/2_What_Drives_Predictions.py", "What Drives Predictions"))
