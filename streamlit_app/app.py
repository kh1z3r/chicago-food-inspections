import streamlit as st

st.set_page_config(
    page_title="Chicago Food Inspections: Fairness Audit",
    page_icon="\U0001F37D️",
    layout="wide",
)

from utils import apply_theme, RED, _star_svg

# Inject the theme once, at the top of every rerun, before the selected page renders.
# This keeps the styling present from the first paint so navigation never flashes unstyled.
apply_theme()

# Sidebar brand, above the auto navigation.
with st.sidebar:
    _stars = "".join(_star_svg(RED, 13) for _ in range(4))
    st.markdown(
        f'<div class="riso-brand"><div class="bstars">{_stars}</div>'
        f'<div class="bmain">AI4ALL</div>'
        f'<div class="bsub">Group 11D</div>'
        f'<div class="bnames">Althan Nguyen, Eva Wonsowicz, Fareeha Gullany, '
        f'Joshua Jacob, Khizer Butt, Snehal Agrawal</div></div>',
        unsafe_allow_html=True,
    )

nav = st.navigation([
    st.Page("home.py", title="Overview", default=True),
    st.Page("pages/1_Model_Performance.py", title="1  Model Performance"),
    st.Page("pages/2_What_Drives_Predictions.py", title="2  What Drives Predictions"),
    st.Page("pages/3_Neighborhood_Effect.py", title="3  Neighborhood Effect"),
    st.Page("pages/4_Threshold_Tuning.py", title="4  Threshold Tuning"),
    st.Page("pages/5_Fairness_Audit.py", title="5  Fairness Audit"),
    st.Page("pages/6_Enforcement_Check.py", title="6  Enforcement Check"),
    st.Page("pages/7_Conclusions.py", title="7  Conclusions"),
])
nav.run()
