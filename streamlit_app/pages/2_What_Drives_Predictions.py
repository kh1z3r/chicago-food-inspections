import streamlit as st
import plotly.express as px
from utils import apply_theme, eyebrow, finding, load_csv, require, BLUE, RED, INK, SLATE, style_figure


eyebrow("Section 2")
st.title("What does the model actually lean on?")
st.markdown(
    """
We use **permutation importance**: shuffle one feature's values in the test set and measure how
much the model's Fail-recall drops. A larger drop indicates the model relied on that feature more.
Each feature is shuffled as a single group, including all ZIP-code columns together.
"""
)

imp = load_csv("permutation_importance.csv")
require(imp, "permutation_importance.csv")

imp = imp.rename(columns={imp.columns[0]: "feature"})
LABELS = {"InspType_g": "Inspection Type", "Zip": "ZIP code",
          "FacilityType_g": "Facility Type", "Risk_g": "Risk level"}
imp["feature"] = imp["feature"].map(LABELS).fillna(imp["feature"])
imp = imp.sort_values("importance", ascending=True)

# one on-system fill; ZIP highlighted red since the narrative singles it out
bar_colors = [RED if f == "ZIP code" else BLUE for f in imp["feature"]]
fig = px.bar(
    imp, x="importance", y="feature", orientation="h",
    labels={"importance": "Drop in Fail-recall when shuffled", "feature": ""},
)
fig.update_traces(marker_color=bar_colors, cliponaxis=False,
                  text=imp["importance"].round(3), textposition="outside",
                  hovertemplate="%{y}<br>Drop in recall: %{x:.3f}<extra></extra>")
style_figure(fig, showlegend=False, xaxis_title="Drop in Fail-recall when shuffled",
             yaxis_title="", height=380)
fig.update_xaxes(range=[0, 0.15])
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Longer bars indicate features the model depends on more. The value is the drop in "
    "Fail-recall when that feature's values are randomly shuffled in the test set."
)

st.divider()

top = imp.sort_values("importance", ascending=False).reset_index(drop=True)
finding(
    f"<b>{top.loc[0, 'feature']}</b> is the most important feature, followed by "
    f"<b>{top.loc[1, 'feature']}</b>. The model relies more on <i>how and why</i> an inspection "
    "is triggered than on the restaurant's own declared risk level. ZIP code outranks the "
    "establishment's assigned risk level, which motivates the neighborhood analysis in the next "
    "section."
)

st.markdown(
    """
This ranking alone does not settle the fairness question. A feature can be important for benign
reasons (it reflects real risk) or for concerning ones (it reflects uneven enforcement). The next
section tests this directly by removing ZIP code entirely and comparing what changes.
"""
)

from utils import page_nav
page_nav(prev=("pages/1_Model_Performance.py", "Model Performance"), next=("pages/3_Neighborhood_Effect.py", "Neighborhood Effect"))
