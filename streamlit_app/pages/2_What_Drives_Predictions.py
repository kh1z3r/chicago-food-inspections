import streamlit as st
import plotly.express as px
from utils import apply_theme, eyebrow, finding, load_csv, require, BLUE, RED, INK, SLATE, style_figure

st.set_page_config(page_title="What Drives Predictions", page_icon="\U0001F37D\uFE0F", layout="wide")
apply_theme()

eyebrow("Section 2")
st.title("What does the model actually lean on?")
st.markdown(
    """
We use **permutation importance**: shuffle one feature's values in the test set and see how
much the model's Fail-recall drops. A bigger drop means the model relied on that feature more.
Each feature — including all the ZIP-code columns together — is shuffled as one group.
"""
)

imp = load_csv("permutation_importance.csv")
require(imp, "permutation_importance.csv")

imp = imp.rename(columns={imp.columns[0]: "feature"})
imp = imp.sort_values("importance", ascending=True)

fig = px.bar(
    imp, x="importance", y="feature", orientation="h",
    color="feature",
    color_discrete_sequence=[INK, SLATE, BLUE, RED],
)
style_figure(
    fig,
    showlegend=False,
    xaxis_title="Drop in Fail-recall when shuffled",
    yaxis_title="",
    height=380,
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

top = imp.sort_values("importance", ascending=False).reset_index(drop=True)
finding(
    f"<b>{top.loc[0, 'feature']}</b> matters most, followed by <b>{top.loc[1, 'feature']}</b>. "
    "The model relies more on <i>how and why</i> an inspection happens than on the "
    "restaurant's own declared risk level — which is exactly why the neighborhood question "
    "(next section) is worth asking: ZIP code outranks the establishment's own assigned "
    "risk level."
)

st.markdown(
    """
This ranking on its own doesn't settle the fairness question — a feature can be
"important" for good reasons (it reflects real risk) or concerning ones (it reflects uneven
enforcement). The next section tests that directly by removing ZIP code entirely and
comparing what changes.
"""
)
