import streamlit as st
import pandas as pd
import plotly.express as px
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, load_parquet, require, BLUE, RED, INK, style_figure

st.set_page_config(
    page_title="Chicago Food Inspections — Audit",
    page_icon="\U0001F37D\uFE0F",
    layout="wide",
)
apply_theme()

# ---- Hero (Soft lockup over Bold stat cards) ----
st.markdown(
    """
<div class="riso-soft riso-hero">
<div class="riso-eyebrow"><span class="riso-halftone tick"></span>GROUP 11D · AI4ALL IGNITE</div>
<h1 class="riso-mis riso-hero-title">Predicting Failure,<br>Auditing Fairness</h1>
<p class="riso-hero-sub">We trained a model to predict which Chicago restaurants fail inspection, then audited who its mistakes fall on. The city already predicts well; the sharper question is <strong>who the model gets wrong, and where.</strong></p>
<p class="riso-hero-team">Nguyen · Wonsowicz · Gullany · Jacob · Butt · Rodas · Agrawal</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---- Headline findings (Bold stat row) ----
h1, h2, h3, h4 = st.columns(4)
with h1:
    stat_card("67%", "chance a passing restaurant is wrongly flagged in the most-flagged ZIP (60620)", tone="red")
with h2:
    stat_card("6%", "the same odds in the Loop downtown", tone="blue")
with h3:
    stat_card("12×", "gap in false-alarm rate, most- vs least-flagged neighborhood", tone="red")
with h4:
    stat_card("24.6%", "of predictions flip when ZIP code is removed from the model", tone="blue")

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

st.divider()

# ---- Dataset stats ----
eyebrow("The Dataset")
st.subheader("City of Chicago · Food Inspections")

c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_card("312,415", "raw inspection records")
with c2:
    stat_card("267,477", "usable after cleaning")
with c3:
    stat_card("22.4%", "citywide fail rate", flag=True)
with c4:
    stat_card("43,356", "distinct establishments")

st.caption(
    "Source: Chicago Data Portal, Chicago Department of Public Health. "
    "Rows without a genuine Pass/Fail decision (Out of Business, No Entry, etc.) are dropped. "
    "Train/test are split by license number so the same restaurant never appears in both."
)

st.divider()

# ---- City map of true fail rate by ZIP ----
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
        m,
        lat="Latitude",
        lon="Longitude",
        color="true_fail_rate",
        size="n_test",
        size_max=28,
        color_continuous_scale=[[0, BLUE], [0.5, "#EFE6C8"], [1, RED]],
        hover_name="Zip",
        hover_data={"true_fail_rate": ":.1%", "n_test": True, "Latitude": False, "Longitude": False},
        zoom=9,
        height=520,
        labels={"true_fail_rate": "Fail rate"},
    )
    style_figure(
        fig,
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Fail rate", tickformat=".0%"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Bubble size = number of test-set inspections in that ZIP. Color = observed fail rate.")
else:
    st.info(
        "Map needs `zip_flip_summary.csv` and `zip_centroids.csv` in `artifacts/`. "
        "See the sidebar pages for findings that don't require the map."
    )

st.divider()

# ---- Roadmap ----
eyebrow("What's in this report")
st.markdown(
    """
Use the sidebar to walk through the analysis in order:

1. **Model Performance** — do the models actually beat guessing?
2. **What Drives Predictions** — which features matter most?
3. **Neighborhood Effect** — does the model lean on ZIP code specifically?
4. **Threshold Tuning** — the recall/false-alarm tradeoff, live
5. **Fairness Audit** — which ZIP codes get over- or under-flagged?
6. **Enforcement Check** — is the gap about food safety, or about who gets inspected?
7. **Conclusions** — what we found, and what we can't claim
"""
)

finding(
    "The headline finding, previewed: ZIP code has a real but modest effect on model "
    "quality — yet it reshuffles roughly a quarter of individual predictions, almost "
    "entirely by lowering flagged risk in low-fail-rate neighborhoods, and the ZIPs with "
    "the highest false-positive rates are also the ones with the most enforcement-heavy "
    "inspection mix."
)
