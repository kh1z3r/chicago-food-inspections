import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_theme, eyebrow, stat_card, finding, load_csv, require, BLUE, RED, INK, NAVY_2, style_figure

eyebrow("The decisive test")
st.title("Is the over-flagging about food safety, or about who gets inspected?")

st.markdown(
    """
Some inspections only happen because of a complaint, or because a restaurant failed before
and is being re-checked. Those visits target places already under suspicion — so a ZIP code
with a lot of these visits can look "worse" in the data even if the food isn't actually worse.

To check this, we ran two tests:
1. Recalculate the false-alarm rate using **only routine, scheduled inspections** — the ones
   nobody specifically flagged.
2. Check whether ZIP codes with more complaint-driven inspections also have more false alarms.
"""
)

cmp = load_csv("zip_enforcement_compare.csv")
require(cmp, "zip_enforcement_compare.csv")
corr = cmp["FPR_all"].corr(cmp["enf_share"])

st.divider()
c1, c2 = st.columns(2)
with c1:
    stat_card("44.5%", "how often the model falsely flags a restaurant, citywide")
with c2:
    stat_card(f"{corr:.2f}", "how closely false alarms track complaint-driven inspections", flag=True)

st.markdown(
    "*(A ZIP code's \"enforcement share\" is the percent of its inspections that were "
    "triggered by a complaint or a re-check — not a routine, scheduled visit.)*"
)

st.divider()
finding(
    "Test 1 result: restricting to only routine inspections doesn't fix the problem — the "
    "false-alarm rate is actually slightly higher (50.2%) than the citywide rate across all "
    "inspection types (44.5%). This tells us the problem isn't caused by complaint-driven "
    "visits skewing the numbers. It shows up even in inspections nobody specifically triggered."
)

st.divider()
eyebrow("Test 2")
st.subheader("Do more complaint-driven inspections mean more false alarms?")

fig = px.scatter(
    cmp, x="enf_share", y="FPR_all", hover_name="Zip",
    color_discrete_sequence=[RED], trendline="ols", trendline_color_override=NAVY_2,
    labels={"enf_share": "Share of inspections that were complaint-driven", "FPR_all": "False-alarm rate"},
    height=440,
)
fig.update_traces(marker=dict(size=9),
                  hovertemplate="ZIP %{hovertext}<br>Complaint-driven share: %{x:.0%}"
                                "<br>False-alarm rate: %{y:.0%}<extra></extra>",
                  selector=dict(mode="markers"))
style_figure(fig, xaxis_tickformat=".0%", yaxis_tickformat=".0%", height=440)
st.plotly_chart(fig, use_container_width=True)



finding(
    f"The more a ZIP code's inspections are complaint-driven, the more "
    f"often that ZIP's restaurants get falsely flagged ({corr:.2f} out of a possible 1.0. "
    " Put simply: it's not just about which restaurants "
    "are riskiest — it's also about how a neighborhood gets policed. This is a pattern, not "
    "proof of cause and effect."
)

from utils import page_nav
page_nav(prev=("pages/5_Fairness_Audit.py", "Fairness Audit"), next=("pages/7_Conclusions.py", "Conclusions"))