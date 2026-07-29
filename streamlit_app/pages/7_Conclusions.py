import streamlit as st
from utils import apply_theme, eyebrow, finding

apply_theme()

eyebrow("Section 7")
st.title("What we found — and what we can't claim")

st.subheader("Findings")
finding(
    "Facility type, risk level, inspection type, and ZIP code carry real predictive signal: "
    "both trained models roughly triple recall over a naive baseline (67&ndash;70% vs. 0%)."
)
finding(
    "The models are poorly calibrated &mdash; their confidence scores overstate risk, "
    "especially at the high end. Treat outputs as a ranking for prioritization, not a "
    "trustworthy probability."
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
    "<i>worse</i>, not better &mdash; a single citywide cutoff can't fix a disparity that "
    "lives at the ZIP level."
)
finding(
    "A ZIP's false-positive rate correlates strongly (0.69) with how enforcement-heavy its "
    "inspection mix is, and the gap persists even when restricted to routine inspections "
    "only &mdash; the strongest evidence here that enforcement patterns, not just food "
    "safety, shape which neighborhoods get flagged."
)

st.divider()
st.subheader("Limitations — what this can't tell you")
st.markdown(
    """
- **Correlation, not causation.** The enforcement-share relationship is a strong association,
  not proof that enforcement intensity *causes* over-flagging rather than both being driven
  by a third factor we haven't measured.
- **Observed fail rate is not the same as true risk.** A low fail rate in a ZIP could reflect
  genuinely safer food, or it could reflect under-inspection — we can't fully separate these
  with this dataset alone.
- **Miscalibrated probabilities.** Neither model's confidence scores should be read as
  literal risk percentages; only the ranked prioritization and the yes/no calls are validated.
- **Precision remains low (~30%) at any threshold we tested that preserves useful recall.**
  Deploying this as-is would mean a majority of flagged restaurants turn out fine.
- **This is retrospective, historical data.** It reflects Chicago's past enforcement patterns
  and can't say whether a *different* inspection policy would produce different outcomes.
"""
)

st.divider()
st.caption(
    "Group 11D · AI4ALL · Data: City of Chicago Food Inspections, Chicago Data Portal "
    "(Chicago Department of Public Health)."
)
