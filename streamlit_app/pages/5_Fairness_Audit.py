import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, SLATE, FLAG_DIVERGING, style_figure

MAP_CONFIG = {"displayModeBar": True, "scrollZoom": True, "displaylogo": False,
              "modeBarButtonsToRemove": ["select2d", "lasso2d"]}


eyebrow("Section 5")
st.title("Which neighborhoods does the model over- or under-flag?")
st.markdown(
    """
At the default 0.5 cutoff, we decompose the model's errors by ZIP code (57 ZIPs with at least
100 test-set inspections). A **false positive** is a restaurant that passed but was flagged as
Fail, representing unearned scrutiny. A **false negative** is a true failure the model cleared,
representing a missed risk.
"""
)

zf = load_csv("zip_fpr_fnr.csv")
require(zf, "zip_fpr_fnr.csv")
zf = zf.sort_values("fpr", ascending=False)

# Citywide FPR is the pooled rate over every test-set inspection, not an average of per-ZIP
# rates. FPR = false positives / actual passes, so it must be aggregated on raw counts; a
# count-weighted mean of per-ZIP FPRs weights by total inspections (passes plus fails) and
# gives a slightly different, incorrect number.
_test = load_parquet("test_predictions.parquet")
if _test is not None:
    _neg = _test["y_true"].values == 0
    overall_fpr = (_test["proba_rf"].values[_neg] >= 0.5).mean()
else:
    overall_fpr = (zf["fpr"] * zf["n_test"]).sum() / zf["n_test"].sum()

c1, c2, c3 = st.columns(3)
with c1:
    stat_card(f"{overall_fpr:.1%}", "citywide false-positive rate")
with c2:
    stat_card(f"{zf['fpr'].max()/overall_fpr:.1f}\u00d7", "worst ZIP's FPR vs. citywide", flag=True)
with c3:
    stat_card(f"{zf['fpr'].min():.1%} \u2013 {zf['fpr'].max():.1%}", "False Positive Rate (FPR) range across ZIPs")

st.divider()
tab1, tab2 = st.tabs(["Chart", "Map"])

with tab1:
    top = zf.head(15)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top["Zip"].astype(str), y=top["fpr"], marker_color=RED, name="FPR",
        text=[f"{v:.0%}" for v in top["fpr"]], textposition="outside", cliponaxis=False,
        hovertemplate="ZIP %{x}<br>False-positive rate: %{y:.1%}<extra></extra>",
    ))
    fig.add_hline(y=overall_fpr, line_dash="dash", line_color=INK,
                  annotation_text=f"citywide FPR = {overall_fpr:.1%}",
                  annotation_font_color=INK)
    style_figure(
        fig,
        xaxis_title="ZIP", yaxis_title="False-positive rate", yaxis_tickformat=".0%",
        height=420,
        title="15 most over-flagged ZIP codes",
    )
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    geo = load_csv("zip_centroids.csv")
    if geo is not None:
        m = zf.copy()
        m["Zip"] = m["Zip"].astype(str)
        g = geo.copy()
        g["Zip"] = g["Zip"].astype(str)
        m = m.merge(g, on="Zip", how="inner")
        fig = px.scatter_mapbox(
            m, lat="Latitude", lon="Longitude", color="fpr", size="n_test", size_max=26,
            color_continuous_scale=FLAG_DIVERGING, color_continuous_midpoint=overall_fpr,
            hover_name="Zip",
            hover_data={"fpr": ":.1%", "fnr": ":.1%", "n_test": True,
                        "Latitude": False, "Longitude": False},
            zoom=9, height=500,
            labels={"fpr": "False-positive rate", "fnr": "False-negative rate",
                    "n_test": "Test inspections"},
        )
        style_figure(fig, mapbox_style="carto-positron", margin=dict(l=0, r=8, t=0, b=0),
                     coloraxis_colorbar=dict(title="FPR", tickformat=".0%"))
        st.plotly_chart(fig, use_container_width=True, config=MAP_CONFIG)
        st.caption(
            f"Diverging scale centered on the citywide FPR ({overall_fpr:.0%}): red = "
            "over-flagged relative to the city, blue = under-flagged. Bubble size = test inspections."
        )
    else:
        from utils import missing_file_notice
        missing_file_notice("zip_centroids.csv")

st.divider()


finding(
    f"The worst ZIP's false-positive rate is <b>{zf['fpr'].max()/overall_fpr:.1f}\u00d7</b> "
    f"the citywide rate ({zf['fpr'].max():.1%} versus {overall_fpr:.1%}), while the lowest is "
    f"near {zf['fpr'].min():.1%}. This is a wide, genuine spread in how often the model flags a "
    "restaurant that in fact passes. It is the concrete evidence behind the second half of the "
    "research question: predicted risk is not distributed evenly across the city." 
    "Section 6 tests whether that cause is enforcement mix."
)

from utils import page_nav
page_nav(prev=("pages/4_Threshold_Tuning.py", "Threshold Tuning"), next=("pages/6_Enforcement_Check.py", "Enforcement Check"))
