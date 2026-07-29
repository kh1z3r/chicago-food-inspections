"""
Shared styling and data-loading helpers for the Chicago Food Inspections app.

Risograph print system (Group 11D). Two spot inks — the Chicago city flag's red and
blue — plus warm black ink on uncoated cream. One token base, one texture dial:
Bold (default, every data surface) and Soft (hero, dividers, icons). Bold keeps
data legible; Soft carries the printed-zine mood. All styling flows through the
tokens below, apply_theme() (CSS), and style_figure() (Plotly), so restyling
happens in one place.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

ARTIFACTS = Path(__file__).parent / "artifacts"

# ---- Ink + paper tokens (exposed for Plotly / page code) ----
INK = "#1B1714"          # warm near-black, all text
INK_SOFT = "#3A342C"     # muted secondary text
BLACK = "#211E1A"        # decorative rules / borders
BLUE = "#0078BF"         # Federal Blue: neutral / baseline / PASS / interactive
BLUE_INK = "#005C93"     # text-safe blue (links)
RED = "#F15060"          # Bright Red: the flagged / over-scrutinised / FAIL signal
RED_INK = "#B02A3A"      # text-safe red
RED_DEEP = "#8E2130"     # red button fill / sequential dark end
PAPER = "#FAF4E6"        # crisp cream, Bold surfaces
PAPER_SOFT = "#F0E9D6"   # worn cream, Soft surfaces
PAPER_PANEL = "#F3ECDA"  # card / panel background
# legacy aliases so older page code keeps importing cleanly
SLATE = INK_SOFT
RED_TEXT = RED_INK
AMBER = "#C89B3C"
FONT = dict(color=INK, family="Archivo, sans-serif")

# Sequential + diverging ramps for per-ZIP magnitude charts
RED_SEQUENTIAL = ["#FCE4E7", "#F5A3AC", "#F15060", "#C23A48", "#8E2130"]
FLAG_DIVERGING = [[0.0, BLUE], [0.5, "#D8D2C4"], [1.0, RED]]


_RISO_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root{
  --riso-red:#F15060; --riso-red-ink:#B02A3A; --riso-red-deep:#8E2130;
  --riso-blue:#0078BF; --riso-blue-ink:#005C93;
  --riso-ink:#1B1714; --riso-ink-soft:#3A342C; --riso-black:#211E1A;
  --paper-bold:#FAF4E6; --paper-soft:#F0E9D6; --paper-panel:#F3ECDA; --knockout:#FFFFFF;

  --grain-bold:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
  --grain-soft:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.5' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
  --grain-opacity:0.05; --grain-tile:var(--grain-bold);
  --mis-offset:1.5px; --halftone-scale:7px; --edge-jitter:0;

  --font-display:'Archivo Black','Arial Black',sans-serif;
  --font-body:'Archivo',system-ui,sans-serif;
  --font-mono:'Space Mono',ui-monospace,monospace;

  --fs-hero:clamp(2.75rem,6vw,4.5rem); --lh-hero:0.95;
  --fs-h1:2.5rem; --fs-h2:1.875rem; --fs-h3:1.375rem;
  --fs-stat:clamp(2.5rem,5vw,3.75rem);
  --fs-body-lg:1.125rem; --fs-body:1rem; --fs-small:0.875rem; --fs-eyebrow:0.75rem;
  --lh-body:1.6; --track-eyebrow:.14em; --track-display:-.01em;

  --line:2px solid var(--riso-ink); --line-heavy:3px solid var(--riso-ink);
  --shadow-print:4px 4px 0 var(--riso-ink);
}

/* ---- paper base + page-wide grain ---- */
.stApp{ background:var(--paper-bold); }
[data-testid="stHeader"]{ background:transparent; }
.stApp::before{
  content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:var(--grain-tile); background-size:140px 140px;
  opacity:var(--grain-opacity); mix-blend-mode:multiply;
}
[data-testid="stAppViewContainer"] > .main{ position:relative; z-index:1; }

/* Soft flips only the intensity tokens; page-wide grain stays low behind copy */
.riso-soft{
  --grain-opacity:0.13; --grain-tile:var(--grain-soft);
  --mis-offset:3px; --halftone-scale:12px; --edge-jitter:0.75px;
}

/* ---- typography ---- */
h1,h2,h3,.riso-display{ font-family:var(--font-display); line-height:1.05;
  letter-spacing:var(--track-display); color:var(--riso-ink); text-transform:uppercase; }
h1{ font-size:var(--fs-h1); } h2{ font-size:var(--fs-h2); } h3{ font-size:var(--fs-h3); }
body,p,li,label,td,.stMarkdown{ font-family:var(--font-body); font-size:var(--fs-body);
  line-height:var(--lh-body); color:var(--riso-ink); }
.riso-num,code,[data-testid="stMetricValue"]{ font-family:var(--font-mono); }

/* ---- misregistration (headings only) ---- */
.riso-mis{ color:var(--riso-ink);
  text-shadow:var(--mis-offset) 0 0 rgba(241,80,96,0.90),
              calc(-1 * var(--mis-offset)) 0 0 rgba(0,120,191,0.85); }
.riso-soft .riso-mis{
  text-shadow:var(--mis-offset) 1px 0.6px rgba(241,80,96,0.80),
              calc(-1 * var(--mis-offset)) -1px 0.6px rgba(0,120,191,0.75); }

/* ---- halftone accents ---- */
.riso-halftone{ background-image:radial-gradient(var(--riso-red) 26%, transparent 27%);
  background-size:var(--halftone-scale) var(--halftone-scale); }
.riso-halftone-duo{
  background-image:radial-gradient(var(--riso-red) 30%, transparent 31%),
                   radial-gradient(var(--riso-blue) 30%, transparent 31%);
  background-size:var(--halftone-scale) var(--halftone-scale);
  background-position:0 0, calc(var(--halftone-scale)/2) calc(var(--halftone-scale)/2); opacity:.85; }

/* ---- hero (Soft) ---- */
.riso-hero{ padding:1.4rem 0 0.4rem; }
.riso-hero-title{ font-family:var(--font-display); text-transform:uppercase;
  font-size:var(--fs-hero); line-height:var(--lh-hero); margin:.15em 0 .35em; }
.riso-hero-sub{ font-family:var(--font-body); font-size:var(--fs-body-lg);
  line-height:1.5; max-width:62ch; color:var(--riso-ink); }
.riso-hero-team{ font-family:var(--font-mono); font-size:var(--fs-small);
  color:var(--riso-ink-soft); letter-spacing:.02em; margin-top:.7rem; }

/* ---- eyebrow ---- */
.riso-eyebrow{ font-family:var(--font-mono); font-size:var(--fs-eyebrow);
  letter-spacing:var(--track-eyebrow); text-transform:uppercase; color:var(--riso-red-ink);
  display:flex; align-items:center; gap:.5rem; margin:.2rem 0 .3rem; }
.riso-eyebrow .tick{ width:28px; height:8px; display:inline-block; }

/* ---- cards / stat cards ---- */
.riso-card{ background:var(--paper-panel); border:var(--line); border-radius:0;
  padding:1.15rem 1.3rem; box-shadow:var(--shadow-print); height:100%; }
.riso-statcard{ border-left:6px solid var(--riso-ink); }
.riso-statcard--red{ border-left-color:var(--riso-red); }
.riso-statcard--blue{ border-left-color:var(--riso-blue); }
.riso-statcard .value{ font-family:var(--font-mono); font-weight:700; font-size:var(--fs-stat);
  line-height:1; color:var(--riso-ink); }
.riso-statcard .label{ font-family:var(--font-body); font-size:var(--fs-small);
  color:var(--riso-ink-soft); margin-top:.45rem; max-width:26ch; }

/* ---- finding callout ---- */
.riso-finding{ background:var(--paper-panel); border:3px solid var(--riso-ink);
  border-left-width:6px; border-radius:0; padding:1rem 1.3rem; margin:.6rem 0 1rem;
  box-shadow:var(--shadow-print); }
.riso-finding.riso-block--red{ border-left-color:var(--riso-red); }
.riso-finding.riso-block--blue{ border-left-color:var(--riso-blue); }
.riso-finding-title{ font-family:var(--font-display); text-transform:uppercase;
  font-size:var(--fs-h3); margin-bottom:.4rem; }
.riso-finding-body{ font-family:var(--font-body); color:var(--riso-ink); line-height:1.55; }

/* ---- buttons / inputs / slider / links ---- */
.stButton>button{ font-family:var(--font-display); text-transform:uppercase; letter-spacing:.03em;
  background:var(--riso-blue); color:var(--knockout); border:var(--line); border-radius:0;
  box-shadow:var(--shadow-print); padding:.6rem 1.1rem;
  transition:transform .12s ease-out, box-shadow .12s ease-out; }
.stButton>button:hover{ transform:translate(2px,2px); box-shadow:2px 2px 0 var(--riso-ink); color:var(--knockout); }
.stButton>button:active{ transform:translate(4px,4px); box-shadow:none; }
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"]>div{
  background:var(--paper-bold); border:var(--line); border-radius:0; color:var(--riso-ink);
  font-family:var(--font-mono); }
:focus-visible{ outline:2px solid var(--riso-blue); outline-offset:2px; }
.stSlider [data-baseweb="slider"] [role="slider"]{ background:var(--riso-blue);
  border:2px solid var(--riso-ink); border-radius:0; }
a,.stMarkdown a{ color:var(--riso-blue-ink); text-decoration:underline;
  text-decoration-thickness:2px; text-underline-offset:3px; }
a:hover{ color:var(--riso-red-ink); }

/* ---- sidebar ---- */
[data-testid="stSidebar"]{ background:var(--paper-panel); border-right:var(--line-heavy); }
[data-testid="stSidebar"] *{ font-family:var(--font-body); color:var(--riso-ink); }

/* ---- dividers ---- */
hr{ border:none; height:3px; background:var(--riso-ink); opacity:.9; }

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{ transition:none!important; animation:none!important; }
  .stButton>button:hover{ transform:none; box-shadow:var(--shadow-print); }
}
"""


def apply_theme(mode="bold"):
    """Inject the Risograph system once at the top of every page. mode='soft'
    is reserved for a page that is entirely voice/mood (no reading copy); pages
    with paragraphs stay Bold and scope Soft to non-paragraph blocks instead."""
    st.markdown(f"<style>{_RISO_CSS}</style>", unsafe_allow_html=True)
    if mode == "soft":
        st.markdown(
            "<style>.stApp{--grain-opacity:.13;--grain-tile:var(--grain-soft);"
            "--mis-offset:3px;--halftone-scale:12px;}</style>",
            unsafe_allow_html=True,
        )


def eyebrow(text):
    st.markdown(
        f'<div class="riso-eyebrow"><span class="riso-halftone tick"></span>{text.upper()}</div>',
        unsafe_allow_html=True,
    )


def stat_card(value, label, tone="ink", flag=False):
    """Bold stat card. tone: 'ink' (neutral), 'red' (a harm metric), 'blue' (a
    baseline metric). Legacy flag=True is treated as tone='red'."""
    if flag:
        tone = "red"
    mod = {"red": " riso-statcard--red", "blue": " riso-statcard--blue"}.get(tone, "")
    st.markdown(
        f'<div class="riso-card riso-statcard{mod}">'
        f'<div class="value">{value}</div>'
        f'<div class="label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def finding(title, body=None, tone="red"):
    """Audit-conclusion callout. Call finding(body) for a bare callout, or
    finding(title, body) for a titled one. tone 'red' = a harm finding,
    'blue' = a baseline finding."""
    if body is None:
        title, body = None, title
    bar = "riso-block--blue" if tone == "blue" else "riso-block--red"
    head = f'<div class="riso-finding-title riso-mis">{title}</div>' if title else ""
    st.markdown(
        f'<div class="riso-finding {bar}">{head}<div class="riso-finding-body">{body}</div></div>',
        unsafe_allow_html=True,
    )


def style_figure(fig, mode="bold", **layout_kwargs):
    """Single source of truth for Plotly styling. Applies the Riso base, then any
    caller layout overrides (map style, margins, colorbar). Every figure passes
    through here so no chart sets its own colors, fonts, or margins inline."""
    paper = PAPER if mode == "bold" else PAPER_SOFT
    base = dict(
        paper_bgcolor=paper,
        plot_bgcolor=paper,
        font=dict(family="Archivo, sans-serif", color=INK, size=13),
        colorway=[BLUE, RED],
        title_font=dict(family="Archivo Black, sans-serif", size=20, color=INK),
        margin=dict(l=56, r=24, t=56, b=48),
        bargap=0.28,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=INK, borderwidth=2),
    )
    base.update(layout_kwargs)
    fig.update_layout(**base)
    fig.update_xaxes(
        showgrid=False, linecolor=INK, linewidth=2, ticks="outside",
        tickfont=dict(family="Space Mono, monospace", size=12, color=INK),
        title_font=dict(color=INK),
    )
    fig.update_yaxes(
        gridcolor="rgba(27,23,20,0.12)", zerolinecolor=INK, linecolor=INK, linewidth=2,
        tickfont=dict(family="Space Mono, monospace", size=12, color=INK),
        title_font=dict(color=INK),
    )
    fig.update_traces(marker_line_color=paper, marker_line_width=2, selector=dict(type="bar"))
    return fig


def label_heatmap_cells(fig, z):
    """Per-cell labels with contrast-aware colors (heatmap textfont is one color)."""
    flat = [v for row in z for v in row]
    mid = (max(flat) + min(flat)) / 2
    x_labels = fig.data[0].x
    y_labels = fig.data[0].y
    for i, row_vals in enumerate(z):
        for j, val in enumerate(row_vals):
            fig.add_annotation(
                x=x_labels[j], y=y_labels[i], text=f"{val:,}", showarrow=False,
                font=dict(color="white" if val > mid else INK, size=13,
                          family="Archivo, sans-serif"),
            )
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
    """Show a standard notice and stop the page if a needed file is missing."""
    if df is None:
        missing_file_notice(name)
        st.stop()
    return df
