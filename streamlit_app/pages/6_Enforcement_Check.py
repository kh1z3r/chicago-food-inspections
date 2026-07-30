import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, require, BLUE, RED, INK, NAVY_2, style_figure


eyebrow("The decisive test")
st.title("Is the over-flagging about food safety, or about who gets inspected?")
st.markdown(
    """
Complaint and Re-Inspection visits target establishments already under suspicion, so a ZIP with
more of those inspection types can appear worse for reasons unrelated to hygiene. We run two
tests: recompute the false-positive rate using **only routine Canvass inspections**, and test
whether a ZIP's overall FPR tracks how **enforcement-heavy** its inspection mix is.
"""
)

cmp = load_csv("zip_enforcement_compare.csv")
require(cmp, "zip_enforcement_compare.csv")

corr = cmp["FPR_all"].corr(cmp["enf_share"])

st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    stat_card("44.5%", "citywide FPR, all inspection types")
with c2:
    stat_card("50.2%", "citywide FPR, Canvass (routine) only", flag=True)
with c3:
    stat_card(f"{corr:.2f}", "corr: ZIP's FPR vs. its enforcement share", flag=True)

st.markdown(
    "*(\"Enforcement share\" = the fraction of a ZIP's test-set inspections that were "
    "Complaint- or Re-Inspection-driven, rather than routine Canvass.)*"
)

st.divider()
eyebrow("Restricting to routine inspections only")
st.subheader("Removing enforcement-triggered visits does not shrink the over-flagging")

st.caption("Top 15 over-flagged ZIPs: all inspection types vs. routine-only Canvass.")
top = cmp.sort_values("FPR_all", ascending=False).head(15)
fig = go.Figure()
fig.add_trace(go.Bar(x=top["Zip"].astype(str), y=top["FPR_all"], name="FPR, all types",
                     marker_color=BLUE,
                     hovertemplate="ZIP %{x}<br>All types: %{y:.1%}<extra></extra>"))
fig.add_trace(go.Bar(x=top["Zip"].astype(str), y=top["FPR_canvass"], name="FPR, Canvass only",
                     marker_color=RED,
                     hovertemplate="ZIP %{x}<br>Canvass only: %{y:.1%}<extra></extra>"))
style_figure(
    fig,
    barmode="group", xaxis_title="ZIP", yaxis_title="False-positive rate", yaxis_tickformat=".0%",
    height=430, margin=dict(l=58, r=26, t=52, b=50),
    legend=dict(orientation="h", y=1.09, x=0, font=dict(color=INK)),
)
fig.update_xaxes(type="category")   # ZIP codes are labels, not a numeric scale
st.plotly_chart(fig, use_container_width=True)

finding(
    "Restricting to routine Canvass inspections does not shrink the gap. If anything, the "
    "spread widens (0.0% to 99% for Canvass-only versus 1.8% to 67.1% across ZIPs for all "
    "types). The over-flagging is not an artifact of complaint-driven visits inflating the "
    "counts; it appears even in inspections that were not specifically triggered."
)

st.divider()
eyebrow("Does enforcement intensity predict the false-positive rate?")
st.subheader("FPR versus enforcement share, by ZIP")

fig = px.scatter(
    cmp, x="enf_share", y="FPR_all", hover_name="Zip",
    color_discrete_sequence=[RED], trendline="ols", trendline_color_override=NAVY_2,
    labels={"enf_share": "Enforcement share (Complaint + Re-Inspection %)", "FPR_all": "False-positive rate"},
    height=440,
)
fig.update_traces(marker=dict(size=9),
                  hovertemplate="ZIP %{hovertext}<br>Enforcement share: %{x:.0%}"
                                "<br>False-positive rate: %{y:.0%}<extra></extra>",
                  selector=dict(mode="markers"))
style_figure(fig, xaxis_tickformat=".0%", yaxis_tickformat=".0%", height=440)
st.plotly_chart(fig, use_container_width=True)

finding(
    f"A ZIP's false-positive rate correlates <b>{corr:.2f}</b> with how enforcement-heavy "
    "its inspection mix is. This is the strongest evidence in the project for the "
    "enforcement-bias hypothesis stated in our proposal: ZIPs with more complaint- and "
    "re-inspection-driven visits are systematically over-flagged as Fail-risk, beyond what "
    "their facility type and risk level alone would predict. This is a correlation, not proof "
    "of causation. It is nonetheless consistent with enforcement intensity itself, not only "
    "underlying food safety, shaping the model's predictions."
)

from utils import page_nav
page_nav(prev=("pages/5_Fairness_Audit.py", "Fairness Audit"), next=("pages/7_Conclusions.py", "Conclusions"))
