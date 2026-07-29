import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, require, BLUE, RED, INK, SLATE, style_figure

st.set_page_config(page_title="Fairness Audit", page_icon="\U0001F37D\uFE0F", layout="wide")
apply_theme()

eyebrow("Section 5")
st.title("Which neighborhoods does the model over- or under-flag?")
st.markdown(
    """
At the default 0.5 cutoff, we break the model's mistakes down by ZIP code (57 ZIPs with at
least 100 test-set inspections). A **false positive** is a restaurant that passed but got
flagged as Fail — unearned scrutiny. A **false negative** is a real Fail the model cleared —
a missed risk.
"""
)

zf = load_csv("zip_fpr_fnr.csv")
require(zf, "zip_fpr_fnr.csv")
zf = zf.sort_values("fpr", ascending=False)

overall_fpr = (zf["fpr"] * zf["n_test"]).sum() / zf["n_test"].sum()
overall_fnr = (zf["fnr"] * zf["n_test"]).sum() / zf["n_test"].sum()

c1, c2, c3 = st.columns(3)
with c1:
    stat_card(f"{overall_fpr:.1%}", "citywide false-positive rate")
with c2:
    stat_card(f"{zf['fpr'].max()/overall_fpr:.1f}\u00d7", "worst ZIP's FPR vs. citywide", flag=True)
with c3:
    stat_card(f"{zf['fpr'].min():.1%} \u2013 {zf['fpr'].max():.1%}", "FPR range across ZIPs")

st.divider()
tab1, tab2 = st.tabs(["Chart", "Map"])

with tab1:
    top = zf.head(15)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top["Zip"].astype(str), y=top["fpr"], marker_color=RED, name="FPR"))
    fig.add_hline(y=overall_fpr, line_dash="dash", line_color=INK,
                  annotation_text=f"citywide FPR = {overall_fpr:.1%}",
                  annotation_font_color=INK)
    style_figure(
        fig,
        xaxis_title="ZIP", yaxis_title="False-positive rate", yaxis_tickformat=".0%",
        height=420,
        title="15 most over-flagged ZIP codes",
    )
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
            color_continuous_scale=[[0, BLUE], [0.5, "#EFE6C8"], [1, RED]],
            hover_name="Zip",
            hover_data={"fpr": ":.1%", "fnr": ":.1%", "n_test": True, "Latitude": False, "Longitude": False},
            zoom=9, height=500, labels={"fpr": "FPR"},
        )
        style_figure(fig, mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        from utils import missing_file_notice
        missing_file_notice("zip_centroids.csv")

st.divider()
eyebrow("Full table")
st.dataframe(
    zf[["Zip", "fpr", "fnr", "n_test"]].style.format({"fpr": "{:.1%}", "fnr": "{:.1%}"}),
    use_container_width=True, height=350,
)

finding(
    f"The worst ZIP's false-positive rate is <b>{zf['fpr'].max()/overall_fpr:.1f}\u00d7</b> "
    f"the citywide rate ({zf['fpr'].max():.1%} vs. {overall_fpr:.1%}), while the best sits "
    f"near {zf['fpr'].min():.1%}. That's a wide, real spread in how often the model cries "
    "wolf on a restaurant that turns out fine &mdash; and it's the concrete evidence behind "
    "the research question's second half: predicted risk is not distributed evenly across "
    "the city, whatever its cause. Section 6 checks whether that cause is enforcement mix."
)
