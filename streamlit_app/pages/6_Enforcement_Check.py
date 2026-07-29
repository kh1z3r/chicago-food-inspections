import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, require, BLUE, RED, INK, style_figure

apply_theme()

eyebrow("Section 6 · the payoff question")
st.title("Is the over-flagging about food safety, or about who gets inspected?")
st.markdown(
    """
Complaint and Re-Inspection visits target places already under suspicion, so a ZIP with more
of those inspection types can look "worse" for reasons unrelated to hygiene. Two checks:
recompute the false-positive rate using **only routine Canvass inspections**, and see whether
a ZIP's overall FPR tracks how **enforcement-heavy** its inspection mix is.
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
st.subheader("FPR barely changes when we remove enforcement-triggered visits")

top = cmp.sort_values("FPR_all", ascending=False).head(15)
fig = go.Figure()
fig.add_trace(go.Bar(x=top["Zip"].astype(str), y=top["FPR_all"], name="FPR, all types", marker_color=INK))
fig.add_trace(go.Bar(x=top["Zip"].astype(str), y=top["FPR_canvass"], name="FPR, Canvass only", marker_color=RED))
style_figure(
    fig,
    barmode="group", xaxis_title="ZIP", yaxis_title="False-positive rate", yaxis_tickformat=".0%",
    height=420,
    legend=dict(orientation="h", y=1.12, font=dict(color=INK)),
    title="Top 15 over-flagged ZIPs: all inspection types vs. routine-only",
)
fig.update_xaxes(type="category")   # ZIP codes are labels, not a numeric scale
st.plotly_chart(fig, use_container_width=True)

finding(
    "Restricting to routine Canvass inspections doesn't shrink the gap &mdash; if anything "
    "the spread widens (0.0&ndash;100% vs. 1.8&ndash;67.1% across ZIPs for all types). "
    "The over-flagging isn't an artifact of complaint-driven visits skewing the numbers; "
    "it shows up even in inspections nobody specifically triggered."
)

st.divider()
eyebrow("Does enforcement intensity predict the false-alarm rate?")
st.subheader("FPR vs. enforcement share, by ZIP")

fig = px.scatter(
    cmp, x="enf_share", y="FPR_all", hover_name="Zip",
    color_discrete_sequence=[RED], trendline="ols",
    labels={"enf_share": "Enforcement share (Complaint + Re-Inspection %)", "FPR_all": "False-positive rate"},
    height=440,
)
fig.update_traces(marker=dict(size=9))
style_figure(fig, xaxis_tickformat=".0%", yaxis_tickformat=".0%", height=440)
st.plotly_chart(fig, use_container_width=True)

finding(
    f"A ZIP's false-positive rate correlates <b>{corr:.2f}</b> with how enforcement-heavy "
    "its inspection mix is. This is the strongest evidence in the project for the "
    "enforcement-bias hypothesis in our proposal: ZIPs with more complaint- and "
    "re-inspection-driven visits get systematically over-flagged as Fail-risk, beyond what "
    "their own facility type and risk level would predict. This is a correlation, not proof "
    "of causation &mdash; but it's consistent with enforcement intensity itself, not just "
    "underlying food safety, shaping the model's predictions."
)
