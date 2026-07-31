import streamlit as st
from utils import apply_theme, eyebrow, finding


eyebrow("Section 7")
st.title("What we found, and what we cannot claim")

st.subheader("Findings")
finding(
    "Facility type, risk level, inspection type, and ZIP code carry real predictive signal: "
    "both trained models catch 67% to 70% of true failures, versus 0% for a naive baseline "
    "that always predicts Pass."
)

finding(
    "Some ZIP codes get false-alarmed far more than others — the worst is 1.5× the citywide rate. "
    "Making the model stricter overall doesn't fix this and actually widens the gap, " 
    "since the neighborhoods already doing well improve even more. "
    "This is a ZIP-level problem, and a citywide fix can't solve it."
)
finding(
    "A ZIP's false-alarm rate closely tracks how much of its inspections are complaint-driven — "
    "and this holds true even when we only look at routine inspections. " 
    "This is our strongest evidence that enforcement patterns, not just food safety, drive which neighborhoods get flagged."
)

st.divider()
st.subheader("Limitations: what this cannot tell you")
st.markdown(
    """
- **Correlation, not causation.** The enforcement-share relationship is a strong association,
  not proof that enforcement intensity *causes* over-flagging rather than both being driven
  by a third factor we have not measured.
- **Observed fail rate is not the same as true risk.** A low fail rate in a ZIP could reflect
  genuinely safer food, or it could reflect under-inspection; we cannot fully separate these
  two explanations with this dataset alone.
- **Precision remains low (approximately 30%) at any threshold we tested that preserves useful
  recall.** Deployed as-is, a majority of flagged restaurants would in fact pass.
- **This is retrospective, historical data.** It reflects Chicago's past enforcement patterns
  and cannot indicate whether a *different* inspection policy would produce different outcomes.
- **Narrow feature set**. We use only four fields: facility type, risk level, inspection type, ZIP code,
  leaving out other relevant data like violation history or building age. More data could improve accuracy, but could make the model better at repeating the same enforcement bias
  we found, instead of fixing it.
"""
)

st.divider()
st.caption(
    "Group 11D, AI4ALL Ignite.  Data: City of Chicago Food Inspections, Chicago Data Portal "
    "(Chicago Department of Public Health)."
)

from utils import page_nav
page_nav(prev=("pages/6_Enforcement_Check.py", "Enforcement Check"))
