import streamlit as st
import plotly.express as px
from utils import (
    eyebrow, star_rule, finding, page_nav, load_csv, style_figure,
    RED, RED_SEQUENTIAL, _star_svg,
)

MAP_CONFIG = {"displayModeBar": True, "scrollZoom": True, "displaylogo": False,
              "modeBarButtonsToRemove": ["select2d", "lasso2d"]}

stars = "".join(_star_svg(RED, 22) for _ in range(4))
st.markdown(
    f"""
<div class="riso-masthead">
<div class="stars">{stars}</div>
<div class="kicker">An AI4ALL Ignite project by Group 11D</div>
<div class="title">Predicting Failure,<br>Auditing Fairness</div>
<div class="sub">We trained a model to predict which Chicago restaurants fail inspection, then audited whom its errors fall on. The model predicts failure well, and the substantive question is <strong>where it errors, and for whom.</strong></div>
<div class="team">Nguyen, Wonsowicz, Gullany, Jacob, Butt, Agrawal</div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
Each year the CDC estimates that roughly **48 million** Americans contract a foodborne illness,
**128,000** are hospitalized, and **3,000** die. Chicago inspects restaurants to detect problems
early, but has far fewer inspectors than visiting every establishment frequently would require, so
prioritizing which establishments to inspect is a consequential decision. We predict inspection
failures from information available *before* the inspection (facility type, risk level, inspection
type, and ZIP code), then test whether those predictions differ across ZIP codes because of genuine
food-safety risk or because of how unevenly enforcement itself is distributed.
"""
)

star_rule()
eyebrow("The Dataset")
st.subheader("City of Chicago Food Inspections")
st.markdown(
    """
<div class="riso-ribbon">
<div class="cell"><div class="v">312,415</div><div class="l">raw inspection records</div></div>
<div class="cell"><div class="v">267,477</div><div class="l">usable after cleaning</div></div>
<div class="cell harm"><div class="v">22.4%</div><div class="l">citywide fail rate</div></div>
<div class="cell"><div class="v">43,356</div><div class="l">distinct establishments</div></div>
</div>
""",
    unsafe_allow_html=True,
)
st.caption(
    "Source: Chicago Data Portal, Chicago Department of Public Health. "
    "Rows without a genuine Pass/Fail decision (Out of Business, No Entry, etc.) are dropped. "
    "Train/test are split by license number so the same restaurant never appears in both."
)

star_rule()
eyebrow("Where failures happen")
st.subheader("Observed fail rate by ZIP code")

flip = load_csv("zip_flip_summary.csv")
geo = load_csv("zip_centroids.csv")
if flip is not None and geo is not None:
    flip = flip.copy()
    geo = geo.copy()
    flip["Zip"] = flip["Zip"].astype(str)
    geo["Zip"] = geo["Zip"].astype(str)
    m = flip.merge(geo, on="Zip", how="inner")
    fig = px.scatter_mapbox(
        m, lat="Latitude", lon="Longitude", color="true_fail_rate", size="n_test",
        size_max=26, color_continuous_scale=RED_SEQUENTIAL, hover_name="Zip",
        hover_data={"true_fail_rate": ":.1%", "n_test": True, "Latitude": False, "Longitude": False},
        zoom=9, height=520,
        labels={"true_fail_rate": "Fail rate", "n_test": "Test inspections"},
    )
    style_figure(
        fig, mapbox_style="carto-positron", margin=dict(l=0, r=8, t=0, b=0),
        coloraxis_colorbar=dict(title="Fail rate", tickformat=".0%"),
    )
    st.plotly_chart(fig, use_container_width=True, config=MAP_CONFIG)
    st.caption("Bubble size = number of test-set inspections in that ZIP (reliability). Color = observed fail rate.")
else:
    st.info("Map needs `zip_flip_summary.csv` and `zip_centroids.csv` in `artifacts/`.")

star_rule()
eyebrow("What's in this report")
st.markdown(
    """
The audit proceeds in order. Use the arrows below or the sidebar to navigate.

1. **Model Performance**: do the trained models outperform a naive baseline?
2. **What Drives Predictions**: which features carry the most signal?
3. **Neighborhood Effect**: does the model depend specifically on ZIP code?
4. **Threshold Tuning**: the recall versus false-positive tradeoff, interactive.
5. **Fairness Audit**: which ZIP codes are over- or under-flagged?
6. **Enforcement Check**: is the disparity driven by food safety or by inspection mix?
7. **Conclusions**: the findings and their limitations.
"""
)


page_nav(next=("pages/1_Model_Performance.py", "Model Performance"))
