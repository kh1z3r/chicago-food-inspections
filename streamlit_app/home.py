import streamlit as st
import plotly.express as px
from utils import (
    eyebrow, star_rule, finding, page_nav, load_csv, style_figure,
    RED, FLAG_DIVERGING, _star_svg,
)

stars = "".join(_star_svg(RED, 22) for _ in range(4))
st.markdown(
    f"""
<div class="riso-masthead">
<div class="stars">{stars}</div>
<div class="kicker">Group 11D · AI4ALL Ignite</div>
<div class="title">Predicting Failure,<br>Auditing Fairness</div>
<div class="sub">We trained a model to predict which Chicago restaurants fail inspection, then audited who its mistakes fall on. The city already predicts well; the sharper question is <strong>who the model gets wrong, and where.</strong></div>
<div class="team">Nguyen · Wonsowicz · Gullany · Jacob · Butt · Rodas · Agrawal</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="riso-ribbon">
<div class="cell harm"><div class="v">67%</div><div class="l">chance a passing restaurant is wrongly flagged in the most-flagged ZIP (60620)</div></div>
<div class="cell"><div class="v">6%</div><div class="l">the same odds in the Loop downtown</div></div>
<div class="cell harm"><div class="v">12×</div><div class="l">gap in false-alarm rate, most- vs least-flagged neighborhood</div></div>
<div class="cell"><div class="v">24.6%</div><div class="l">of predictions flip when ZIP is removed from the model</div></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
Every year the CDC estimates roughly **48 million** Americans get sick, **128,000** are
hospitalized, and **3,000** die from foodborne illness. Chicago inspects restaurants to catch
problems early, but with far too few inspectors to visit every kitchen often, so *where* to send
them first is a real, high-stakes question. We predict inspection failures from information
available *before* the inspection (facility type, risk level, inspection type, and ZIP), then ask
whether those predictions differ across ZIP codes because of real food-safety risk, or because of
how unevenly enforcement itself is distributed.
"""
)

star_rule()
eyebrow("The Dataset")
st.subheader("City of Chicago · Food Inspections")
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
        size_max=26, color_continuous_scale=FLAG_DIVERGING, hover_name="Zip",
        hover_data={"true_fail_rate": ":.1%", "n_test": True, "Latitude": False, "Longitude": False},
        zoom=9, height=520, labels={"true_fail_rate": "Fail rate"},
    )
    style_figure(
        fig, mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Fail rate", tickformat=".0%"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Bubble size = number of test-set inspections in that ZIP. Color = observed fail rate.")
else:
    st.info("Map needs `zip_flip_summary.csv` and `zip_centroids.csv` in `artifacts/`.")

star_rule()
eyebrow("What's in this report")
st.markdown(
    """
Walk the audit in order, using the arrows below or the sidebar:

1. **Model Performance** — do the models actually beat guessing?
2. **What Drives Predictions** — which features matter most?
3. **Neighborhood Effect** — does the model lean on ZIP code specifically?
4. **Threshold Tuning** — the recall / false-alarm tradeoff, live
5. **Fairness Audit** — which ZIP codes get over- or under-flagged?
6. **Enforcement Check** — is the gap about food safety, or about who gets inspected?
7. **Conclusions** — what we found, and what we can't claim
"""
)
finding(
    "The headline, previewed: ZIP code barely improves the model overall, yet it reshuffles "
    "roughly a quarter of individual predictions, almost entirely by lowering flagged risk in "
    "low-fail-rate neighborhoods, and the ZIPs with the highest false-positive rates are the "
    "same ones with the most enforcement-heavy inspection mix."
)

page_nav(next=("pages/1_Model_Performance.py", "Model Performance"))
