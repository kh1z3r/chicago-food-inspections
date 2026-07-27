"""
Shared styling and data-loading helpers for the Chicago Food Inspections app.

Design system (civic audit-report look, built around the Chicago flag palette):
  ink        #14213D  - headers, primary text
  paper      #F5F3EE  - page/card background
  flag-blue  #2EA3D6  - neutral / "pass" / informational accent
  flag-red   #C60C30  - risk / "fail" / flag accent
  slate      #3D4550  - secondary text, gridlines (darkened for contrast)
  red-text   #9B0A26  - red accent text on light backgrounds
  amber      #C89B3C  - sparing highlight (thresholds, callouts)

Type: "Source Serif 4" for display/headlines, "IBM Plex Sans" for body,
"IBM Plex Mono" for stat figures, ZIP codes, and table numerals.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

ARTIFACTS = Path(__file__).parent / "artifacts"

INK = "#14213D"
PAPER = "#F5F3EE"
BLUE = "#2EA3D6"
RED = "#C60C30"
SLATE = "#3D4550"
RED_TEXT = "#9B0A26"
AMBER = "#C89B3C"
BLACK = "#000000"

FONT = dict(color=INK, family="IBM Plex Sans, sans-serif")


def style_figure(fig, **layout_kwargs):
    """Apply consistent readable text styling to a Plotly figure."""
    fig.update_layout(
        font=FONT,
        plot_bgcolor="white",
        paper_bgcolor="white",
        **layout_kwargs,
    )
    fig.update_xaxes(tickfont=dict(color=INK), title_font=dict(color=INK))
    fig.update_yaxes(tickfont=dict(color=INK), title_font=dict(color=INK))
    if fig.layout.coloraxis:
        cbar = fig.layout.coloraxis.colorbar
        title_cfg = dict(font=dict(color=INK))
        if cbar.title and cbar.title.text:
            title_cfg["text"] = cbar.title.text
        fig.update_layout(
            coloraxis_colorbar=dict(
                tickfont=dict(color=INK),
                title=title_cfg,
            )
        )
    return fig


def label_heatmap_cells(fig, z):
    """Add per-cell labels with contrast-aware colors (heatmap textfont only supports one color)."""
    flat = [v for row in z for v in row]
    mid = (max(flat) + min(flat)) / 2
    x_labels = fig.data[0].x
    y_labels = fig.data[0].y
    for i, row_vals in enumerate(z):
        for j, val in enumerate(row_vals):
            fig.add_annotation(
                x=x_labels[j],
                y=y_labels[i],
                text=f"{val:,}",
                showarrow=False,
                font=dict(
                    color="white" if val > mid else INK,
                    size=13,
                    family="IBM Plex Sans, sans-serif",
                ),
            )
    return fig


def apply_theme():
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
            color: {INK};
        }}
        .stApp {{
            background-color: {PAPER};
        }}
        h1, h2, h3 {{
            font-family: 'Source Serif 4', serif !important;
            color: {INK} !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em;
        }}
        h1 {{
            border-bottom: 3px solid {RED};
            padding-bottom: 0.35em;
        }}
        p, li, ol, ul {{
            color: {BLACK};
        }}
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] ol,
        [data-testid="stMarkdownContainer"] ul {{
            color: {BLACK};
        }}
        [data-testid="stCaptionContainer"] {{
            color: {SLATE} !important;
        }}
        .eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.75rem;
            color: {RED_TEXT};
            font-weight: 600;
            margin-bottom: -0.6em;
            display: block;
        }}
        .stat-card {{
            background: white;
            border: 1px solid #E3DFD3;
            border-left: 4px solid {BLUE};
            border-radius: 4px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.6rem;
        }}
        .stat-card.flag {{ border-left-color: {RED}; }}
        .stat-card .big {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 2rem;
            font-weight: 600;
            color: {INK};
            line-height: 1.1;
        }}
        .stat-card .label {{
            font-size: 0.85rem;
            color: {SLATE};
            margin-top: 0.2rem;
        }}
        .finding {{
            background: white;
            border: 1px solid #E3DFD3;
            border-radius: 4px;
            padding: 1rem 1.3rem;
            margin: 0.8rem 0 1.2rem 0;
            color: {BLACK};
        }}
        .finding .star {{
            color: {RED_TEXT};
            font-family: 'IBM Plex Mono', monospace;
        }}
        [data-testid="stSidebar"] {{
            background-color: {INK};
        }}
        [data-testid="stSidebar"] * {{
            color: {PAPER} !important;
        }}
        [data-testid="stMetricValue"] {{
            font-family: 'IBM Plex Mono', monospace;
            color: {INK};
        }}
        code, .stCode {{
            font-family: 'IBM Plex Mono', monospace;
        }}
        hr {{
            border-color: #E3DFD3;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def eyebrow(text):
    st.markdown(f'<span class="eyebrow">{text}</span>', unsafe_allow_html=True)


def stat_card(value, label, flag=False):
    cls = "stat-card flag" if flag else "stat-card"
    st.markdown(
        f'<div class="{cls}"><div class="big">{value}</div>'
        f'<div class="label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def finding(text):
    st.markdown(
        f'<div class="finding"><span class="star">&#9733;</span> {text}</div>',
        unsafe_allow_html=True,
    )


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
    """Show a standard notice and stop rendering the rest of the page if a needed file is missing."""
    if df is None:
        missing_file_notice(name)
        st.stop()
    return df
