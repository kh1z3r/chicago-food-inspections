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
    "The models are poorly calibrated: their probability estimates overstate risk, especially "
    "at the high end. Treat the outputs as a ranking for prioritization, not as trustworthy "
    "probabilities."
)
finding(
    "Inspection type and ZIP code drive predictions more than the restaurant's own declared "
    "risk level does."
)
finding(
    "ZIP code's effect on overall model quality is modest (a ~5% relative PR-AUC drop when "
    "removed) but concentrated and directional: it reshuffles about a quarter of individual "
    "predictions, almost entirely by lowering flagged risk in already-low-fail-rate ZIPs."
)
finding(
    "False-positive rates vary widely by ZIP (the worst is roughly 1.5&times; the citywide "
    "rate), and tightening the global decision threshold makes this neighborhood gap "
    "<i>worse</i>, not better. A single citywide cutoff cannot correct a disparity that "
    "operates at the ZIP level."
)
finding(
    "A ZIP's false-positive rate correlates strongly (0.69) with how enforcement-heavy its "
    "inspection mix is, and the gap persists even when restricted to routine inspections only. "
    "This is the strongest evidence here that enforcement patterns, not only food safety, shape "
    "which neighborhoods are flagged."
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
- **Miscalibrated probabilities.** Neither model's probability estimates should be read as
  literal risk percentages; only the ranked prioritization and the Pass/Fail classifications
  are validated.
- **Precision remains low (approximately 30%) at any threshold we tested that preserves useful
  recall.** Deployed as-is, a majority of flagged restaurants would in fact pass.
- **This is retrospective, historical data.** It reflects Chicago's past enforcement patterns
  and cannot indicate whether a *different* inspection policy would produce different outcomes.
"""
)

st.divider()
st.caption(
    "Group 11D, AI4ALL Ignite.  Data: City of Chicago Food Inspections, Chicago Data Portal "
    "(Chicago Department of Public Health)."
)

from utils import page_nav
page_nav(prev=("pages/6_Enforcement_Check.py", "Enforcement Check"))
