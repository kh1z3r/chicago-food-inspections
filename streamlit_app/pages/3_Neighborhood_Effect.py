import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import average_precision_score
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, RED_SEQUENTIAL, style_figure

MAP_CONFIG = {"displayModeBar": True, "scrollZoom": True, "displaylogo": False,
              "modeBarButtonsToRemove": ["select2d", "lasso2d"]}


eyebrow("The core fairness question")
st.title("Does the model actually use the neighborhood?")
st.markdown(
    """
We trained the same Random Forest twice on the identical split, once **with** ZIP code as a
feature and once **without**, then compared them by **PR-AUC** (precision-recall area under the
curve) rather than recall alone. """
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
    f"about a 5% relative change), so ZIP is not the dominant driver of overall model quality. "
    f"However, <b>{flipped.mean():.1%} of individual predictions flip</b> when ZIP is removed. "
    "Many restaurants sit near the 0.5 decision boundary, so even a small probability shift is "
    "enough to change the classification. Overall quality moves little, but <i>which</i> "
    "restaurants are flagged changes substantially."
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
            color_continuous_scale=RED_SEQUENTIAL,
            hover_name="Zip",
            hover_data={"flip_rate": ":.1%", "true_fail_rate": ":.1%", "n_test": True,
                        "Latitude": False, "Longitude": False},
            zoom=9, height=520,
            labels={"flip_rate": "Flip rate", "true_fail_rate": "True fail rate",
                    "n_test": "Test inspections"},
        )
        style_figure(fig, mapbox_style="carto-positron", margin=dict(l=0, r=8, t=0, b=0),
                     coloraxis_colorbar=dict(title="Flip rate", tickformat=".0%"))
        st.plotly_chart(fig, use_container_width=True, config=MAP_CONFIG)
        st.caption("Bubble size = number of test-set inspections in the ZIP; "
                   "color = share of predictions that flip when ZIP is dropped.")
    else:
        from utils import missing_file_notice
        missing_file_notice("zip_centroids.csv")

with tab2:
    tbl = flip_df[["Zip", "n_test", "true_fail_rate", "flip_rate",
                   "flip_up_rate", "flip_down_rate"]].head(20).copy()
    tbl["Zip"] = tbl["Zip"].astype(str)
    tbl = tbl.rename(columns={
        "Zip": "ZIP", "n_test": "Test inspections", "true_fail_rate": "True fail rate",
        "flip_rate": "Flip rate", "flip_up_rate": "Flip up", "flip_down_rate": "Flip down",
    })
    st.dataframe(
        tbl.style.format({
            "True fail rate": "{:.1%}", "Flip rate": "{:.1%}",
            "Flip up": "{:.1%}", "Flip down": "{:.1%}",
        }),
        use_container_width=True, hide_index=True,
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
    "Flips are almost entirely one-directional: adding ZIP predominantly makes the model "
    f"<b>more lenient</b> ({down_avg:.1%} flip down versus only {up_avg:.1%} flip up). The "
    f"lenient effect is strongest in ZIP codes that already have low real fail rates ({corr:.2f})</b>. "
    "Zip codes aren't randomly nudging predictions around, they are specifically dialing back a 'Fail' prediction "
    " that other features would have arrived towards."
)

st.markdown(
    """
    We only know how often a ZIP code actually fails based on past inspections
    and how often an area gets inspected, and how thoroughly, is not the same everywhere.
    A ZIP code with low fail rates could mean it has safer restaurants, or it could mean it
    is inspected less often, so problems don't get caught and recorded in the first place. 
    This gets further investigated in Section 5.
"""
)

from utils import page_nav
page_nav(prev=("pages/1_Model_Performance.py", "Model Performance"), next=("pages/4_Threshold_Tuning.py", "Threshold Tuning"))
