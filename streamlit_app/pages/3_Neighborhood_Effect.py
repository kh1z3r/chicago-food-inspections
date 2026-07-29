import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import average_precision_score
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, style_figure


eyebrow("Section 3 · the core fairness question")
st.title("Does the model actually use the neighborhood?")
st.markdown(
    """
We trained the same Random Forest twice on the identical split — once **with** ZIP code as a
feature, once **without** — and compared them with **PR-AUC** (precision-recall area under
the curve), not recall alone. Recall at a single cutoff is misleading here: removing a
feature can shift precision and recall in opposite directions without the model actually
getting better or worse. PR-AUC summarizes quality across every possible cutoff at once, and
it's the right lens for imbalanced data like this (22% Fail) since it isn't diluted by the
huge number of easy true negatives.
"""
)

test = load_parquet("test_predictions.parquet")
require(test, "test_predictions.parquet")

y = test["y_true"].values
pr_with = average_precision_score(y, test["proba_rf"])
pr_without = average_precision_score(y, test["proba_rf_no_zip"])

pred_with = (test["proba_rf"] >= 0.5).astype(int)
pred_without = (test["proba_rf_no_zip"] >= 0.5).astype(int)
flipped = pred_with != pred_without

st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    stat_card(f"{pr_with:.3f}", "PR-AUC with ZIP")
with c2:
    stat_card(f"{pr_without:.3f}", "PR-AUC without ZIP")
with c3:
    stat_card(f"{flipped.mean():.1%}", "predictions that flip when ZIP is dropped", flag=True)

finding(
    f"PR-AUC drops only modestly when ZIP is removed ({pr_with:.3f} &rarr; {pr_without:.3f}, "
    f"about a 5% relative change) &mdash; ZIP is not the dominant driver of overall model "
    f"quality. But <b>{flipped.mean():.1%} of individual predictions flip</b> when ZIP is "
    "removed. Many restaurants sit near the 0.5 decision boundary, so even a small shift "
    "from adding ZIP is enough to flip the call for a lot of them &mdash; overall quality "
    "barely moves, but <i>who</i> gets flagged shifts substantially."
)

st.divider()
eyebrow("Where the flips happen")
st.subheader("ZIP-level flip breakdown")

flip_df = load_csv("zip_flip_summary.csv")
require(flip_df, "zip_flip_summary.csv")
flip_df = flip_df.sort_values("flip_rate", ascending=False)

geo = load_csv("zip_centroids.csv")

tab1, tab2 = st.tabs(["Map", "Table"])

with tab1:
    if geo is not None:
        m = flip_df.copy()
        m["Zip"] = m["Zip"].astype(str)
        g = geo.copy()
        g["Zip"] = g["Zip"].astype(str)
        m = m.merge(g, on="Zip", how="inner")
        fig = px.scatter_mapbox(
            m, lat="Latitude", lon="Longitude",
            color="flip_rate", size="n_test", size_max=26,
            color_continuous_scale=[[0, "#EFE6C8"], [1, RED]],
            hover_name="Zip",
            hover_data={"flip_rate": ":.1%", "true_fail_rate": ":.1%", "n_test": True,
                        "Latitude": False, "Longitude": False},
            zoom=9, height=520, labels={"flip_rate": "Flip rate"},
        )
        style_figure(fig, mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        from utils import missing_file_notice
        missing_file_notice("zip_centroids.csv")

with tab2:
    st.dataframe(
        flip_df[["Zip", "n_test", "true_fail_rate", "flip_rate", "flip_up_rate", "flip_down_rate"]]
        .head(20).style.format({
            "true_fail_rate": "{:.1%}", "flip_rate": "{:.1%}",
            "flip_up_rate": "{:.1%}", "flip_down_rate": "{:.1%}",
        }),
        use_container_width=True,
    )

st.divider()
eyebrow("Direction of the flips")

corr = flip_df["flip_rate"].corr(flip_df["true_fail_rate"])
up_avg = flip_df["flip_up_rate"].mean()
down_avg = flip_df["flip_down_rate"].mean()

c1, c2, c3 = st.columns(3)
with c1:
    stat_card(f"{up_avg:.1%}", "avg. flip UP (ZIP adds scrutiny)")
with c2:
    stat_card(f"{down_avg:.1%}", "avg. flip DOWN (ZIP removes scrutiny)", flag=True)
with c3:
    stat_card(f"{corr:.2f}", "correlation: flip rate vs. true fail rate")

finding(
    "Flips are almost entirely one-directional: adding ZIP mostly makes the model "
    f"<b>more lenient</b> ({down_avg:.1%} flip down vs. only {up_avg:.1%} flip up). And the "
    f"correlation between flip rate and true fail rate is <b>strongly negative ({corr:.2f})</b>: "
    "ZIP changes predictions the most in neighborhoods that <i>already</i> have the lowest "
    "observed fail rates &mdash; it acts like a local base-rate correction, pulling down "
    "over-predictions in low-fail-rate areas rather than adding scrutiny elsewhere."
)

st.markdown(
    """
That's a more reassuring pattern than "ZIP is inflating risk in poor neighborhoods" &mdash;
but it comes with a caveat central to this whole project: an *observed* fail rate reflects
both true food safety **and** how much a neighborhood gets inspected and how. A low
observed rate could mean genuinely safer food, or it could mean a ZIP is under-inspected and
its problems simply aren't being found. Section 6 tests this directly.
"""
)

from utils import page_nav
page_nav(prev=("pages/2_What_Drives_Predictions.py", "What Drives Predictions"), next=("pages/4_Threshold_Tuning.py", "Threshold Tuning"))
