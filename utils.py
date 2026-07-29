"""
Shared styling and data-loading helpers for the Chicago Food Inspections app.

Chicago-flag design system (Group 11D). Deep navy is the identity (masthead,
sidebar, dividers, footer); flag red is the accent and the "over-flagged / FAIL"
signal; six-point stars are the recurring Chicago mark; data lives on a clean
near-white so charts and tables stay razor-legible. Everything flows through the
tokens below, apply_theme() (CSS) and style_figure() (Plotly), so restyling
happens in one place.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

ARTIFACTS = Path(__file__).parent / "artifacts"

# ---- palette tokens (exposed for Plotly / page code) ----
NAVY = "#0A2A4A"         # identity: masthead, sidebar, dividers, footer
NAVY_2 = "#123A63"       # lighter navy: chart bars, hover, secondary
NAVY_DEEP = "#07203A"    # depth / heavy borders
RED = "#C8102E"          # Chicago flag red: stars, the harm / over-flagged signal
RED_INK = "#A20C24"      # red text on white (AA)
INK = "#15181C"          # near-black body text on white
INK_SOFT = "#4B5158"     # secondary text, captions
PAPER = "#FCFCFA"        # near-white data surface (clean, not cream)
PANEL = "#FFFFFF"        # card fill
PANEL_2 = "#F1F3F6"      # subtle gray panel
LINE = "#D7DCE3"         # light rule
WHITE = "#FFFFFF"
# legacy aliases so older page code keeps importing cleanly
BLUE = NAVY_2
BLUE_INK = NAVY
SLATE = INK_SOFT
RED_TEXT = RED_INK
BLACK = INK
PAPER_SOFT = PAPER
PAPER_PANEL = PANEL_2
AMBER = "#C8102E"
FONT = dict(color=INK, family="Archivo, sans-serif")

# sequential + diverging ramps for per-ZIP magnitude charts
RED_SEQUENTIAL = ["#FBE3E7", "#EF9AA6", "#DB4A5E", "#C8102E", "#8E0B20"]
FLAG_DIVERGING = [[0.0, NAVY_2], [0.5, "#E9ECF0"], [1.0, RED]]


def _star_svg(color=RED, size=14):
    """A single Chicago six-point star as inline SVG."""
    pts = ("12,1 14.75,7.24 21.53,6.5 17.5,12 21.53,17.5 14.75,16.76 "
           "12,23 9.25,16.76 2.47,17.5 6.5,12 2.47,6.5 9.25,7.24")
    return (f'<svg class="riso-star" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'aria-hidden="true"><polygon points="{pts}" fill="{color}"/></svg>')


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root{
  --navy:#0A2A4A; --navy-2:#123A63; --navy-deep:#07203A;
  --red:#C8102E; --red-ink:#A20C24;
  --ink:#15181C; --ink-soft:#4B5158;
  --paper:#FCFCFA; --panel:#FFFFFF; --panel-2:#F1F3F6; --line:#D7DCE3; --white:#FFFFFF;

  --font-display:'Archivo Black','Arial Black',sans-serif;
  --font-body:'Archivo',system-ui,sans-serif;
  --font-mono:'Space Mono',ui-monospace,monospace;

  --fs-hero:clamp(2.6rem,5.4vw,4rem); --fs-h1:2.1rem; --fs-h2:1.6rem; --fs-h3:1.22rem;
  --fs-stat:clamp(1.7rem,2.3vw,2.35rem);
  --fs-body-lg:1.1rem; --fs-body:1rem; --fs-small:0.875rem; --fs-eyebrow:0.72rem;
  --lh-body:1.62; --track-eyebrow:.16em;
  --space-section:2.6rem;
}

/* ---- force the light Chicago paper to win over OS dark mode / config ---- */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{ background:var(--paper); }
.stApp h1,.stApp h2,.stApp h3,.stApp h4,[data-testid="stHeading"],[data-testid="stHeading"] *{ color:var(--navy)!important; }
.stApp [data-testid="stMarkdownContainer"] p,.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] strong,.stApp [data-testid="stMarkdownContainer"] em{ color:var(--ink); }
[data-testid="stHeader"],[data-testid="stToolbar"]{ background:transparent!important; }
[data-testid="stHeader"] *,[data-testid="stToolbar"] *{ color:var(--navy)!important; fill:var(--navy)!important; }
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *{ color:var(--ink-soft)!important; }
[data-testid="stAlert"]{ background:var(--panel-2); border:1px solid var(--line); border-radius:0; color:var(--ink); }

/* ---- typography ---- */
h1,h2,h3,h4,.riso-display{ font-family:var(--font-display); color:var(--navy);
  letter-spacing:-.01em; line-height:1.08; }
h1{ font-size:var(--fs-h1); margin-top:.2rem; } h2{ font-size:var(--fs-h2); }
h3{ font-size:var(--fs-h3); }
body,p,li,label,td,.stMarkdown{ font-family:var(--font-body); font-size:var(--fs-body);
  line-height:var(--lh-body); color:var(--ink); }
.riso-num,code,[data-testid="stMetricValue"]{ font-family:var(--font-mono); }
.stApp [data-testid="stMarkdownContainer"] p{ margin-bottom:1rem; }

/* ---- section spacing + rules ---- */
hr{ border:none; height:2px; background:var(--navy); opacity:1; margin:var(--space-section) 0 1.4rem; }
[data-testid="stMain"] .block-container{ padding-top:2.2rem; max-width:1180px; }

/* ---- eyebrow (clean red label, no dot tick) ---- */
.riso-eyebrow{ font-family:var(--font-mono); font-size:var(--fs-eyebrow);
  letter-spacing:var(--track-eyebrow); text-transform:uppercase; color:var(--red-ink);
  font-weight:700; margin:0 0 .35rem; }

/* ---- masthead (navy flag band) ---- */
.riso-masthead{ background:var(--navy); color:var(--white); border-radius:0;
  padding:2.1rem 2.4rem 2.3rem; margin:0 0 1.9rem; border-left:8px solid var(--red); }
.riso-masthead .stars{ display:flex; gap:.5rem; margin-bottom:1rem; }
.riso-masthead .kicker{ font-family:var(--font-mono); font-size:var(--fs-eyebrow);
  letter-spacing:var(--track-eyebrow); text-transform:uppercase; color:#9DB6D2; font-weight:700; }
.riso-masthead .title{ font-family:var(--font-display); text-transform:uppercase;
  font-size:var(--fs-hero); line-height:.98; color:var(--white); margin:.5rem 0 .7rem; }
.riso-masthead .sub{ font-family:var(--font-body); font-size:var(--fs-body-lg);
  line-height:1.5; color:#D7E2EF; max-width:64ch; }
.riso-masthead .sub strong{ color:var(--white); }
.riso-masthead .team{ font-family:var(--font-mono); font-size:var(--fs-small);
  color:#8AA6C6; margin-top:1rem; letter-spacing:.02em; }

/* ---- editorial stat ribbon (replaces generic card grid) ---- */
.riso-ribbon{ display:grid; grid-template-columns:repeat(4,1fr); gap:0;
  border:2px solid var(--navy); border-radius:0; background:var(--panel); margin:.2rem 0 1.4rem; }
.riso-ribbon .cell{ padding:1.15rem 1.25rem; border-left:1px solid var(--line); }
.riso-ribbon .cell:first-child{ border-left:none; }
.riso-ribbon .cell.harm{ box-shadow:inset 4px 0 0 var(--red); }
.riso-ribbon .v{ font-family:var(--font-mono); font-weight:700; font-size:var(--fs-stat);
  line-height:1; color:var(--navy); white-space:nowrap; letter-spacing:-.02em; }
.riso-ribbon .cell.harm .v{ color:var(--red-ink); }
.riso-ribbon .l{ font-family:var(--font-body); font-size:var(--fs-small);
  color:var(--ink-soft); margin-top:.5rem; line-height:1.4; }
@media (max-width:820px){ .riso-ribbon{ grid-template-columns:repeat(2,1fr); }
  .riso-ribbon .cell:nth-child(3){ border-left:none; } }

/* ---- stat card (kept for pages that call stat_card) ---- */
.riso-card{ background:var(--panel); border:2px solid var(--navy); border-radius:0;
  padding:1.15rem 1.3rem; height:100%; display:flex; flex-direction:column; }
.riso-statcard{ box-shadow:inset 5px 0 0 var(--navy); min-height:150px; }
.riso-statcard--red{ box-shadow:inset 5px 0 0 var(--red); }
.riso-statcard .value{ font-family:var(--font-mono); font-weight:700; font-size:var(--fs-stat);
  line-height:1; color:var(--navy); white-space:nowrap; letter-spacing:-.02em; }
.riso-statcard--red .value{ color:var(--red-ink); }
.riso-statcard .label{ font-family:var(--font-body); font-size:var(--fs-small);
  color:var(--ink-soft); margin-top:.55rem; line-height:1.4; }

/* ---- finding callout ---- */
.riso-finding{ background:var(--panel); border:2px solid var(--navy); border-radius:0;
  padding:1.1rem 1.35rem; margin:1rem 0 1.3rem; box-shadow:inset 6px 0 0 var(--red);
  display:flex; gap:.9rem; align-items:flex-start; }
.riso-finding.baseline{ box-shadow:inset 6px 0 0 var(--navy); }
.riso-finding .riso-star{ flex:0 0 auto; margin-top:.15rem; }
.riso-finding-title{ font-family:var(--font-display); color:var(--navy);
  font-size:var(--fs-h3); margin-bottom:.35rem; }
.riso-finding-body{ font-family:var(--font-body); color:var(--ink); line-height:1.55; }

/* ---- star divider ---- */
.riso-rule{ display:flex; align-items:center; gap:.8rem; margin:var(--space-section) 0 1.3rem; }
.riso-rule .bar{ flex:1; height:2px; background:var(--navy); }

/* ---- buttons / inputs / slider / links ---- */
.stButton>button{ font-family:var(--font-display); text-transform:uppercase; letter-spacing:.03em;
  background:var(--navy); color:var(--white); border:2px solid var(--navy); border-radius:0;
  padding:.55rem 1.1rem; transition:background .12s ease-out; }
.stButton>button:hover{ background:var(--navy-2); color:var(--white); border-color:var(--navy-2); }
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"]>div{
  background:var(--panel); border:2px solid var(--navy); border-radius:0; color:var(--ink);
  font-family:var(--font-mono); }
:focus-visible{ outline:2px solid var(--red); outline-offset:2px; }
.stSlider [data-baseweb="slider"] [role="slider"]{ background:var(--red);
  border:2px solid var(--navy); border-radius:0; }
a,.stMarkdown a{ color:var(--navy); text-decoration:underline; text-decoration-thickness:2px;
  text-underline-offset:3px; }
a:hover{ color:var(--red-ink); }

/* ---- sidebar (navy identity). Do NOT set font-family on icon spans. ---- */
[data-testid="stSidebar"]{ background:var(--navy); border-right:3px solid var(--red); }
/* lift the brand (user content) above the auto navigation */
[data-testid="stSidebar"] div:has(> [data-testid="stSidebarNav"]){ display:flex; flex-direction:column; }
[data-testid="stSidebarUserContent"]{ order:1; padding-top:0; }
[data-testid="stSidebarNav"]{ order:2; }
[data-testid="stSidebar"] a,[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,[data-testid="stSidebarNav"] span{ color:#E7EEF6!important; }
[data-testid="stSidebarNav"]{ padding-top:.2rem; }
[data-testid="stSidebarNav"] a{ font-family:var(--font-body); font-size:1rem;
  line-height:1.3; padding:.46rem .8rem; }
[data-testid="stSidebarNav"] a p,[data-testid="stSidebarNav"] a span:not([data-testid]){
  font-size:1rem; margin:0; }
[data-testid="stSidebarNav"] a:hover{ background:rgba(255,255,255,.07); }
[data-testid="stSidebarNav"] a[aria-current="page"]{ color:var(--white)!important; font-weight:600;
  background:rgba(255,255,255,.10); box-shadow:inset 3px 0 0 rgba(255,255,255,.55); }
[data-testid="stSidebar"] [data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] *{ color:#E7EEF6!important; }

/* ---- plotly chart frame (border-box so it never triggers an inner scrollbar) ---- */
[data-testid="stPlotlyChart"]{ border:2px solid var(--navy); background:var(--panel);
  box-sizing:border-box; overflow:hidden; }
[data-testid="stPlotlyChart"] .modebar{ display:none!important; }

/* ---- prev / next page nav (button-like, edge-aligned, hover-fill) ---- */
.riso-pagenav{ border-top:2px solid var(--navy); margin-top:var(--space-section); margin-bottom:.4rem; }
[data-testid="stPageLink"]{ margin-top:1rem; }
[data-testid="stPageLink"] a{ display:inline-flex; align-items:center; gap:.55rem;
  border:2px solid var(--navy); background:var(--panel); padding:.65rem 1.25rem; box-sizing:border-box;
  font-family:var(--font-display); text-transform:uppercase; font-size:.92rem; letter-spacing:.03em;
  color:var(--navy)!important; transition:border-color .14s ease, color .14s ease; }
[data-testid="stColumn"]:last-child [data-testid="stVerticalBlock"]:has([data-testid="stPageLink"]){ align-items:flex-end; }
[data-testid="stPageLink"] a:hover{ border-color:var(--red); color:var(--red-ink)!important; background:var(--panel); }
[data-testid="stPageLink"] a:hover p{ color:var(--red-ink)!important; }
[data-testid="stPageLink"] a p{ color:inherit!important; font-size:.92rem; margin:0; }

/* ---- sidebar brand (above the nav) ---- */
.riso-brand{ padding:1.05rem .95rem .85rem; margin-bottom:.5rem;
  border-bottom:1px solid rgba(255,255,255,.16); }
.riso-brand .bstars{ display:flex; gap:.3rem; margin-bottom:.55rem; }
.riso-brand .bmain{ font-family:var(--font-display); text-transform:uppercase;
  font-size:1.55rem; color:var(--white); line-height:1; letter-spacing:.005em; }
.riso-brand .bsub{ font-family:var(--font-mono); font-size:.7rem; text-transform:uppercase;
  letter-spacing:.14em; color:#9DB6D2; margin-top:.5rem; }
.riso-brand .bnames{ font-family:var(--font-body); font-size:.72rem; line-height:1.55;
  color:#B9C9DC; margin-top:.75rem; }

/* ---- minimal page transition ---- */
[data-testid="stMain"] .block-container{ animation:riso-fade .28s ease-out; }
@keyframes riso-fade{ from{ opacity:0; transform:translateY(5px); } to{ opacity:1; transform:none; } }

@media (prefers-reduced-motion:reduce){ *,*::before,*::after{ transition:none!important; animation:none!important; } }
"""


def apply_theme(mode="light"):
    """Inject the Chicago-flag system once at the top of the app / each page."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def eyebrow(text):
    st.markdown(f'<div class="riso-eyebrow">{text.upper()}</div>', unsafe_allow_html=True)


def star_rule():
    """A navy rule with a single red Chicago star, as a section marker."""
    st.markdown(f'<div class="riso-rule"><span class="bar"></span>{_star_svg(RED, 16)}'
                f'<span class="bar"></span></div>', unsafe_allow_html=True)


def page_nav(prev=None, next=None):
    """Prev / next links at the foot of a page so readers don't need the sidebar.
    prev and next are (page_path, label) tuples."""
    st.markdown('<div class="riso-pagenav"></div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    if prev:
        with left:
            try:
                st.page_link(prev[0], label=f"←  {prev[1]}")
            except Exception:
                pass
    if next:
        with right:
            try:
                st.page_link(next[0], label=f"{next[1]}  →")
            except Exception:
                pass


def stat_card(value, label, tone="navy", flag=False):
    """Stat card. tone 'red'/flag=True = a harm metric; anything else = navy baseline."""
    if flag or tone == "red":
        mod = " riso-statcard--red"
    else:
        mod = ""
    st.markdown(
        f'<div class="riso-card riso-statcard{mod}">'
        f'<div class="value">{value}</div><div class="label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def finding(title, body=None, tone="red"):
    """Audit-conclusion callout. finding(body) for a bare callout, finding(title, body)
    for a titled one. tone 'red' = a harm finding, 'baseline'/'navy' = a baseline finding."""
    if body is None:
        title, body = None, title
    cls = "baseline" if tone in ("baseline", "navy", "blue") else ""
    star = _star_svg(NAVY if cls else RED, 20)
    head = f'<div class="riso-finding-title">{title}</div>' if title else ""
    st.markdown(
        f'<div class="riso-finding {cls}">{star}<div>{head}'
        f'<div class="riso-finding-body">{body}</div></div></div>',
        unsafe_allow_html=True,
    )


def style_figure(fig, mode="light", **layout_kwargs):
    """Single source of truth for Plotly styling. Chicago navy + flag red, framed."""
    base = dict(
        paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(family="Archivo, sans-serif", color=INK, size=13),
        colorway=[NAVY_2, RED],
        margin=dict(l=58, r=26, t=54, b=50), bargap=0.3,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=NAVY, borderwidth=1),
    )
    base.update(layout_kwargs)
    fig.update_layout(**base)
    # a title-less chart must never render the JS string "undefined"; normalize + style
    fig.update_layout(title=dict(text=fig.layout.title.text or "",
                      font=dict(family="Archivo Black, sans-serif", size=18, color=NAVY)))
    # mirror=True draws the axis line on all four sides -> a clean box frame
    fig.update_xaxes(showgrid=False, linecolor=NAVY, linewidth=1.5, mirror=True, ticks="outside",
                     tickfont=dict(family="Space Mono, monospace", size=12, color=INK),
                     title_font=dict(color=NAVY, size=13))
    fig.update_yaxes(gridcolor="rgba(10,42,74,0.10)", zerolinecolor=NAVY, linecolor=NAVY,
                     linewidth=1.5, mirror=True,
                     tickfont=dict(family="Space Mono, monospace", size=12, color=INK),
                     title_font=dict(color=NAVY, size=13))
    fig.update_traces(marker_line_color=PANEL, marker_line_width=1.5, selector=dict(type="bar"))
    return fig


def label_heatmap_cells(fig, z):
    flat = [v for row in z for v in row]
    mid = (max(flat) + min(flat)) / 2
    x_labels = fig.data[0].x
    y_labels = fig.data[0].y
    for i, row_vals in enumerate(z):
        for j, val in enumerate(row_vals):
            fig.add_annotation(x=x_labels[j], y=y_labels[i], text=f"{val:,}", showarrow=False,
                               font=dict(color="white" if val > mid else INK, size=13,
                                         family="Archivo, sans-serif"))
    return fig


def missing_file_notice(name):
    st.warning(
        f"**Missing artifact:** `artifacts/{name}` wasn't found. "
        f"Export it from the Colab notebook and drop it into the `artifacts/` "
        f"folder next to `app.py`, then rerun."
    )


@st.cache_data
def load_csv(name, **kwargs):
    path = ARTIFACTS / name
    if not path.exists():
        return None
    return pd.read_csv(path, **kwargs)


@st.cache_data
def load_parquet(name):
    path = ARTIFACTS / name
    if not path.exists():
        return None
    return pd.read_parquet(path)


def require(df, name):
    if df is None:
        missing_file_notice(name)
        st.stop()
    return df
