import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime
import io
import requests as _req

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="FinVault · AI Budget Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# GLOBAL THEME — Black + Neon Green/Gold Glassmorphism
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Boot animation overlay ── */
#fv-boot {
    position: fixed; inset: 0; z-index: 99999;
    background: #050505;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: bootFade 0.5s ease 2.8s forwards;
}
@keyframes bootFade { to { opacity: 0; pointer-events: none; } }

.boot-logo {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem; font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #00e5a0, #c8a800, #00e5a0);
    background-size: 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 1.8s ease infinite;
    margin-bottom: 0.4rem;
}
@keyframes shimmer { 0%,100%{background-position:0%} 50%{background-position:100%} }

.boot-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem; color: #444;
    letter-spacing: 0.2em; margin-bottom: 2.5rem;
}
.boot-bar-wrap {
    width: 220px; height: 3px;
    background: rgba(255,255,255,0.07);
    border-radius: 999px; overflow: hidden;
    margin-bottom: 1.2rem;
}
.boot-bar {
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #00e5a0, #c8a800);
    border-radius: 999px;
    animation: barFill 2.2s cubic-bezier(0.4,0,0.2,1) 0.3s forwards;
}
@keyframes barFill { to { width: 100%; } }

.boot-ticker {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; color: #333;
    letter-spacing: 0.06em;
    animation: tickerAnim 2.4s steps(1) 0.3s forwards;
}
@keyframes tickerAnim {
    0%  { content: ""; }
    20% { color: #00e5a0; }
}

.boot-chart {
    display: flex; align-items: flex-end; gap: 5px;
    height: 40px; margin-bottom: 1.5rem;
}
.boot-bar-c {
    width: 8px; border-radius: 3px 3px 0 0;
    animation: barUp 0.6s ease forwards;
    opacity: 0;
}
.boot-bar-c:nth-child(1){height:30%;background:#00e5a0;animation-delay:0.1s}
.boot-bar-c:nth-child(2){height:55%;background:#c8a800;animation-delay:0.2s}
.boot-bar-c:nth-child(3){height:40%;background:#00e5a0;animation-delay:0.3s}
.boot-bar-c:nth-child(4){height:75%;background:#c8a800;animation-delay:0.4s}
.boot-bar-c:nth-child(5){height:60%;background:#00e5a0;animation-delay:0.5s}
.boot-bar-c:nth-child(6){height:90%;background:#c8a800;animation-delay:0.6s}
.boot-bar-c:nth-child(7){height:70%;background:#00e5a0;animation-delay:0.7s}
@keyframes barUp { to { opacity: 1; } }

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #080808 !important;
    color: #e8e8e8 !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #080808 !important; }
[data-testid="block-container"] { padding-top: 1.5rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid rgba(0,229,160,0.1) !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── Radio — completely override Streamlit default highlight ── */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 2px !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 7px 14px 7px 10px !important;
    margin: 1px 0 !important;
    cursor: pointer !important;
    transition: background 0.18s !important;
    width: 100% !important;
    display: flex !important; align-items: center !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span,
[data-testid="stSidebar"] [role="radiogroup"] label div {
    color: #777 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover p,
[data-testid="stSidebar"] [role="radiogroup"] label:hover span {
    color: #00e5a0 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(0,229,160,0.07) !important;
}
/* Hide the ugly radio circle */
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}
/* Selected state */
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] {
    background: rgba(0,229,160,0.1) !important;
    border-radius: 10px !important;
    border-left: 3px solid #00e5a0 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] p,
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] span {
    color: #00e5a0 !important;
    font-weight: 700 !important;
}

/* ── Inputs — full mobile override ── */
/* Force dark mode on all input elements across all browsers/devices */
input, textarea, select,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #1a1a1a !important;
    background-color: #1a1a1a !important;
    border: 1.5px solid rgba(0,229,160,0.3) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #00e5a0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    opacity: 1 !important;
    appearance: none !important;
    -webkit-appearance: none !important;
}
/* Placeholder */
input::placeholder, textarea::placeholder,
[data-testid="stTextInput"] input::placeholder,
[data-testid="stNumberInput"] input::placeholder {
    color: #666 !important;
    -webkit-text-fill-color: #666 !important;
    opacity: 1 !important;
}
/* Focus */
input:focus, textarea:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    background: #222222 !important;
    background-color: #222222 !important;
    border-color: #00e5a0 !important;
    box-shadow: 0 0 0 2px rgba(0,229,160,0.18) !important;
    outline: none !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* Password dots visible */
input[type="password"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #1a1a1a !important;
}
/* Autofill — prevent white flash on mobile Chrome */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 9999px #1a1a1a inset !important;
    box-shadow: 0 0 0 9999px #1a1a1a inset !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #00e5a0 !important;
    background-color: #1a1a1a !important;
    color: #ffffff !important;
}
/* Input wrapper backgrounds */
[data-baseweb="input"],
[data-baseweb="base-input"],
[data-testid="stTextInput"] > div,
[data-testid="stNumberInput"] > div,
[data-testid="stTextArea"] > div {
    background: #1a1a1a !important;
    background-color: #1a1a1a !important;
    border-radius: 10px !important;
}
/* Selectbox */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-baseweb="select"] > div {
    background: #1a1a1a !important;
    background-color: #1a1a1a !important;
    border: 1.5px solid rgba(0,229,160,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
[data-baseweb="select"] *, [data-baseweb="select"] span { color: #e8e8e8 !important; }
/* Button text fix on mobile */
.stButton > button * { color: #080808 !important; -webkit-text-fill-color: #080808 !important; }
/* Labels */
label, [data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #888 !important;
    -webkit-text-fill-color: #888 !important;
    font-size: 0.82rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00e5a0 0%, #c8a800 100%) !important;
    color: #080808 !important; font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.52rem 1.6rem !important;
    letter-spacing: 0.04em !important; font-size: 0.88rem !important;
    box-shadow: 0 0 18px rgba(0,229,160,0.2) !important;
    transition: box-shadow 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    box-shadow: 0 0 28px rgba(0,229,160,0.38) !important;
    transform: translateY(-1px) !important;
}
.stDownloadButton > button {
    background: rgba(0,229,160,0.08) !important;
    border: 1px solid rgba(0,229,160,0.3) !important;
    color: #00e5a0 !important; border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(0,229,160,0.1) !important;
    border-radius: 16px !important; padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 1.45rem !important; color: #00e5a0 !important;
}
[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.76rem !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,229,160,0.08) !important;
    border-radius: 12px !important; overflow: hidden !important;
}

/* ── Progress bars ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg,#00e5a0,#c8a800) !important;
    border-radius: 999px !important;
}
[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.05) !important; border-radius: 999px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.018) !important;
    border: 1px solid rgba(0,229,160,0.08) !important; border-radius: 12px !important;
}
[data-testid="stExpander"] summary { color: #aaa !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important; border: none !important;
    background: rgba(255,255,255,0.03) !important;
}
[data-testid="stAlert"] p { color: #bbb !important; }

/* ── Form ── */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.018) !important;
    border: 1px solid rgba(0,229,160,0.08) !important;
    border-radius: 16px !important; padding: 1.2rem !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,229,160,0.08) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #00e5a0; border-radius: 4px; }

/* ══════════════════════════════════════
   MOBILE RESPONSIVE + FULL UI OVERHAUL
   ══════════════════════════════════════ */

/* ── Page fade transition ── */
[data-testid="stMainBlockContainer"] {
    animation: pageFadeIn 0.35s ease-out !important;
}
@keyframes pageFadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Ticker bar ── */
.fv-ticker-wrap {
    overflow: hidden; width: 100%;
    background: rgba(0,229,160,0.05);
    border-top: 1px solid rgba(0,229,160,0.1);
    border-bottom: 1px solid rgba(0,229,160,0.1);
    padding: 6px 0; margin-bottom: 1.2rem;
}
.fv-ticker {
    display: inline-block;
    white-space: nowrap;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #00e5a0;
    letter-spacing: 0.06em;
    animation: tickerScroll 28s linear infinite;
}
@keyframes tickerScroll {
    from { transform: translateX(100vw); }
    to   { transform: translateX(-100%); }
}

/* ── Mobile bottom nav ── */
.fv-bottom-nav {
    display: none;
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
    background: #0a0a0a;
    border-top: 1px solid rgba(0,229,160,0.12);
    padding: 8px 0 env(safe-area-inset-bottom, 8px);
    justify-content: space-around; align-items: center;
}
.fv-bottom-nav a {
    display: flex; flex-direction: column; align-items: center;
    gap: 3px; text-decoration: none; color: #555;
    font-family: 'DM Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.04em; padding: 4px 8px;
    border-radius: 8px; transition: color 0.15s;
}
.fv-bottom-nav a.active, .fv-bottom-nav a:hover { color: #00e5a0; }
.fv-bottom-nav a svg { width: 20px; height: 20px; stroke-width: 1.5; }

/* ── Responsive KPI grid ── */
.fv-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.2rem;
}
.fv-kpi-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(0,229,160,0.1);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.15s;
}
.fv-kpi-card:hover {
    border-color: rgba(0,229,160,0.25);
    transform: translateY(-2px);
}
.fv-kpi-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.4), transparent);
}
.fv-kpi-card::after {
    content: "";
    position: absolute; top: -30px; right: -20px;
    width: 80px; height: 80px; border-radius: 50%;
    opacity: 0.06;
}
.fv-kpi-income::after  { background: #00e5a0; }
.fv-kpi-expense::after { background: #ff6060; }
.fv-kpi-savings::after { background: #c8a800; }
.fv-kpi-score::after   { background: #00d2ff; }
.fv-kpi-tag {
    font-family: 'DM Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.1em; font-weight: 600;
    padding: 2px 8px; border-radius: 999px; margin-bottom: 6px;
    display: inline-block;
}
.fv-kpi-val {
    font-family: 'DM Mono', monospace; font-size: 1.55rem;
    font-weight: 500; letter-spacing: -0.02em; line-height: 1.1;
    margin: 2px 0;
}
.fv-kpi-label {
    font-size: 0.68rem; color: #555; font-family: 'DM Mono', monospace;
    text-transform: uppercase; letter-spacing: 0.07em;
}
.fv-sparkline {
    margin-top: 8px; opacity: 0.7;
}

/* ── Glass chart card ── */
.fv-chart-card {
    background: rgba(255,255,255,0.018);
    border: 1px solid rgba(0,229,160,0.08);
    border-radius: 18px;
    padding: 1.2rem 1.4rem 0.8rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative; overflow: hidden;
}
.fv-chart-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.25), transparent);
}
.fv-chart-card:hover { border-color: rgba(0,229,160,0.15); }

/* ── Hero greeting card ── */
.fv-hero {
    background: linear-gradient(135deg,
        rgba(0,229,160,0.07) 0%,
        rgba(200,168,0,0.05) 50%,
        rgba(0,0,0,0) 100%);
    border: 1px solid rgba(0,229,160,0.12);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.4rem;
    position: relative; overflow: hidden;
}
.fv-hero::after {
    content: "";
    position: absolute; top: -60px; right: -40px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,229,160,0.08) 0%, transparent 70%);
}
.fv-hero-greeting {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: clamp(1.4rem, 4vw, 2rem);
    background: linear-gradient(90deg, #00e5a0, #c8a800, #ffffff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.02em;
}
.fv-hero-sub {
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: #555; letter-spacing: 0.06em; margin-top: 4px;
}
.fv-hero-stats {
    display: flex; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap;
}
.fv-hero-stat {
    display: flex; flex-direction: column;
}
.fv-hero-stat-val {
    font-family: 'DM Mono', monospace; font-size: 1.1rem;
    font-weight: 500; color: #00e5a0;
}
.fv-hero-stat-lbl {
    font-size: 0.65rem; color: #444; font-family: 'DM Mono', monospace;
    text-transform: uppercase; letter-spacing: 0.08em;
}

/* ══════════════════════════════════════
   MOBILE BREAKPOINTS
   ══════════════════════════════════════ */
@media (max-width: 768px) {
    /* Show bottom nav on mobile */
    .fv-bottom-nav { display: flex !important; }
    /* Add bottom padding so content isn't hidden behind bottom nav */
    [data-testid="stMainBlockContainer"] {
        padding-bottom: 80px !important;
    }
    /* Stack KPI grid 2 cols on mobile */
    .fv-kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
    }
    .fv-kpi-val { font-size: 1.15rem !important; }
    .fv-hero-greeting { font-size: 1.4rem !important; }
    .fv-hero { padding: 1.1rem 1.2rem !important; }
    .fv-page-title { font-size: 1.4rem !important; }
    /* Sidebar hidden on mobile by default — use bottom nav */
    [data-testid="stSidebar"] {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    /* Charts full width on mobile */
    .fv-chart-card { padding: 0.9rem 0.8rem 0.5rem !important; }
    /* Ticker smaller on mobile */
    .fv-ticker { font-size: 0.65rem !important; }
}
@media (max-width: 480px) {
    /* Single col KPIs on very small screens */
    .fv-kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    .fv-kpi-val { font-size: 1rem !important; }
    .fv-hero-stats { gap: 1rem !important; }
}

/* ── Custom classes ── */
.fv-page-title {
    font-family: 'Syne', sans-serif; font-size: 1.85rem;
    font-weight: 800; letter-spacing: -0.025em;
    background: linear-gradient(90deg, #00e5a0 0%, #c8a800 55%, #e8e8e8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.1rem;
}
.fv-page-sub {
    font-size: 0.78rem; color: #444; margin-bottom: 1.4rem;
    font-family: 'DM Mono', monospace; letter-spacing: 0.05em;
}
.glass-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(0,229,160,0.1);
    border-radius: 18px; padding: 1.4rem 1.6rem;
    margin-bottom: 1rem; position: relative; overflow: hidden;
}
.glass-card::after {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,transparent,rgba(0,229,160,0.35),transparent);
}
.kpi-pill {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.67rem; font-weight: 500; padding: 2px 10px;
    border-radius: 999px; letter-spacing: 0.07em; margin-bottom: 6px;
}
.kpi-pill-green { background: rgba(0,229,160,0.09); color: #00e5a0; border: 1px solid rgba(0,229,160,0.22); }
.kpi-pill-gold  { background: rgba(200,168,0,0.1);  color: #c8a800; border: 1px solid rgba(200,168,0,0.28); }
.kpi-pill-red   { background: rgba(255,80,80,0.09); color: #ff6060; border: 1px solid rgba(255,80,80,0.22); }
.kpi-pill-cyan  { background: rgba(0,210,255,0.09); color: #00d2ff; border: 1px solid rgba(0,210,255,0.22); }
.kpi-big {
    font-family: 'DM Mono', monospace; font-size: 1.8rem;
    font-weight: 500; letter-spacing: -0.02em; line-height: 1; margin: 4px 0 2px;
}
.kpi-label-sm {
    font-size: 0.7rem; color: #444; font-family: 'DM Mono', monospace;
    letter-spacing: 0.07em; text-transform: uppercase;
}
.section-tag {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.65rem; font-weight: 600; padding: 2px 10px;
    border-radius: 999px; background: rgba(0,229,160,0.07);
    color: #00e5a0; border: 1px solid rgba(0,229,160,0.18);
    letter-spacing: 0.1em; margin-bottom: 3px; text-transform: uppercase;
}
.fv-section-title {
    font-family: 'Syne', sans-serif; font-size: 1.02rem;
    font-weight: 700; color: #d8d8d8; margin-bottom: 0.8rem;
}
.sidebar-logo {
    font-family: 'Syne', sans-serif; font-size: 1.35rem; font-weight: 800;
    background: linear-gradient(90deg, #00e5a0, #c8a800);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.02em; padding: 0.6rem 0 0.15rem;
}
.sidebar-tagline {
    font-size: 0.66rem; color: #333; font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em; margin-bottom: 1rem;
}
.user-badge {
    background: rgba(0,229,160,0.06); border: 1px solid rgba(0,229,160,0.15);
    border-radius: 10px; padding: 8px 12px; font-family: 'DM Mono', monospace;
    font-size: 0.78rem; color: #00e5a0; margin-bottom: 0.8rem; letter-spacing: 0.03em;
}
.budget-bar-bg {
    background: rgba(255,255,255,0.05); border-radius: 999px;
    height: 7px; margin: 4px 0 14px; overflow: hidden;
}
.budget-bar-fill { height: 7px; border-radius: 999px; transition: width 0.6s ease; }
.invest-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(0,229,160,0.08);
    border-radius: 14px; padding: 0.9rem 1.1rem; margin-bottom: 0.55rem; transition: border-color 0.2s;
}
.invest-card:hover { border-color: rgba(0,229,160,0.28); }
.invest-name { font-weight: 700; font-size: 0.9rem; color: #e0e0e0; margin-bottom: 2px; }
.invest-desc { font-size: 0.76rem; color: #555; font-family: 'DM Mono', monospace; }
.home-feature {
    background: rgba(255,255,255,0.018); border: 1px solid rgba(0,229,160,0.07);
    border-radius: 12px; padding: 0.85rem 1rem; margin-bottom: 0.45rem;
    font-size: 0.86rem; color: #999; display: flex; gap: 10px; align-items: center;
}
.home-feature span { color: #00e5a0; font-size: 1.05rem; }
</style>
""", unsafe_allow_html=True)

# ── Boot animation (shown once per session) ──
if "booted" not in st.session_state:
    st.session_state.booted = True
    st.markdown("""
<div id="fv-boot">
  <div class="boot-chart">
    <div class="boot-bar-c"></div><div class="boot-bar-c"></div>
    <div class="boot-bar-c"></div><div class="boot-bar-c"></div>
    <div class="boot-bar-c"></div><div class="boot-bar-c"></div>
    <div class="boot-bar-c"></div>
  </div>
  <div class="boot-logo">FinVault</div>
  <div class="boot-tag">// AI BUDGET PLANNER — INITIALISING</div>
  <div class="boot-bar-wrap"><div class="boot-bar"></div></div>
  <div class="boot-ticker" id="bt">LOADING MARKETS...</div>
</div>
<script>
const msgs = ["LOADING MARKETS...","SYNCING PORTFOLIO...","CRUNCHING NUMBERS...","READY ✓"];
let i=0;
const el = document.getElementById("bt");
if(el){ const t=setInterval(()=>{ i++; if(i<msgs.length){el.textContent=msgs[i];} else clearInterval(t); },600); }
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────
BG       = "#080808"
PLOT_BG  = "#0d0d0d"
GRID     = "rgba(255,255,255,0.05)"
FONT_C   = "#c8c8c8"
GREEN    = "#00e5a0"
GOLD     = "#c8a800"
RED      = "#ff5050"
CYAN     = "#00dcff"
PURPLE   = "#a855f7"
PALETTE  = [GREEN, GOLD, CYAN, RED, PURPLE, "#fb923c", "#34d399", "#60a5fa"]

def plotly_base(height=320):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=PLOT_BG,
        font=dict(family="DM Mono, monospace", color=FONT_C, size=11),
        margin=dict(l=12, r=12, t=28, b=12),
        xaxis=dict(gridcolor=GRID, showline=False, zeroline=False, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID, showline=False, zeroline=False, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), orientation="h",
                    y=-0.18, x=0.5, xanchor="center"),
        hoverlabel=dict(bgcolor="#111", font_color="#e8e8e8", bordercolor=GREEN),
        height=height,
    )

# ─────────────────────────────────────────
# SUPABASE REST CLIENT (no extra package)
# ─────────────────────────────────────────
_SB_URL = "https://lfoheejwfwhlfnhgbryk.supabase.co"
_SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxmb2hlZWp3ZndobGZuaGdicnlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA2MzQ3OTQsImV4cCI6MjA5NjIxMDc5NH0.pJ3tXA0csJmmwVdrU_9MGwBYIXpNvci8w2C43_7IF70"
_HEADERS = {
    "apikey": _SB_KEY,
    "Authorization": f"Bearer {_SB_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def _url(table): return f"{_SB_URL}/rest/v1/{table}"

def sb_select(table, filters=None, order=None):
    params = {"select": "*"}
    if filters:
        params.update(filters)
    if order:
        params["order"] = order
    r = _req.get(_url(table), headers=_HEADERS, params=params)
    return r.json() if r.ok else []

def sb_insert(table, data):
    r = _req.post(_url(table), headers=_HEADERS, json=data)
    return r.json() if r.ok else []

def sb_update(table, data, filters):
    r = _req.patch(_url(table), headers={**_HEADERS, "Prefer": "return=minimal"},
                   json=data, params=filters)
    return r.ok

def sb_delete(table, filters):
    r = _req.delete(_url(table), headers=_HEADERS, params=filters)
    return r.ok

def sb_upsert(table, data, on_conflict):
    h = {**_HEADERS, "Prefer": f"resolution=merge-duplicates,return=minimal"}
    r = _req.post(_url(table), headers=h, json=data,
                  params={"on_conflict": on_conflict})
    return r.ok

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
for k, v in [("logged_in", False), ("user_id", None), ("username", "")]:
    if k not in st.session_state: st.session_state[k] = v

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
CURRENCY_RATES = {
    "INR 🇮🇳": 1.0, "USD 🇺🇸": 83.50, "EUR 🇪🇺": 90.20,
    "GBP 🇬🇧": 105.80, "JPY 🇯🇵": 0.555, "AUD 🇦🇺": 54.30,
    "CAD 🇨🇦": 61.20, "CHF 🇨🇭": 93.10, "CNY 🇨🇳": 11.50,
    "SGD 🇸🇬": 61.80, "AED 🇦🇪": 22.73, "SAR 🇸🇦": 22.26,
    "HKD 🇭🇰": 10.68, "MYR 🇲🇾": 17.70, "NZD 🇳🇿": 50.10,
}

def load_transactions(uid):
    rows = sb_select("transactions", {"user_id": f"eq.{uid}"}, order="date.desc")
    if rows:
        df = pd.DataFrame(rows)
        df = df.rename(columns={
            "id":"ID","type":"Type","category":"Category","amount":"Amount",
            "date":"Date","description":"Description","is_recurring":"Recurring",
            "recur_freq":"Frequency","currency":"Currency","amount_inr":"Amount_INR"
        })
        # Keep only needed columns, fill missing
        for col in ["ID","Type","Category","Amount","Date","Description","Recurring","Frequency","Currency","Amount_INR"]:
            if col not in df.columns: df[col] = "" if col in ["Description","Frequency","Currency"] else 0
        df["Date"] = pd.to_datetime(df["Date"])
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        df["Amount_INR"] = pd.to_numeric(df["Amount_INR"], errors="coerce").fillna(df["Amount"])
        df["Recurring"] = df["Recurring"].fillna(0).astype(int)
        return df[["ID","Type","Category","Amount","Date","Description","Recurring","Frequency","Currency","Amount_INR"]]
    return pd.DataFrame(columns=["ID","Type","Category","Amount","Date",
                                  "Description","Recurring","Frequency","Currency","Amount_INR"])

def load_budgets(uid, month):
    rows = sb_select("budgets", {"user_id": f"eq.{uid}", "month": f"eq.{month}"})
    return {r["category"]: r["amount"] for r in rows}

def compute_health_score(df):
    if df.empty: return 0, {}
    inc = df[df["Type"]=="Income"]["Amount_INR"].sum()
    exp = df[df["Type"]=="Expense"]["Amount_INR"].sum()
    if inc == 0: return 0, {}
    sr = (inc - exp) / inc
    er = exp / inc
    s1 = min(25, sr * 100)
    s2 = max(0, min(25, 25 - (er - 0.5) * 50))
    s3 = min(25, df[df["Type"]=="Income"]["Category"].nunique() * 8)
    df2 = df.copy(); df2["M"] = df2["Date"].dt.to_period("M")
    s4 = min(25, df2["M"].nunique() * 5)
    return round(s1+s2+s3+s4), {"Savings rate": round(s1,1), "Expense control": round(s2,1),
                                  "Income diversity": round(s3,1), "Consistency": round(s4,1)}

def predict_savings(df, ahead=3):
    if df.empty: return []
    d = df.copy(); d["M"] = d["Date"].dt.to_period("M")
    m = d.groupby(["M","Type"])["Amount_INR"].sum().unstack(fill_value=0).reset_index()
    if "Income" not in m.columns or "Expense" not in m.columns: return []
    m["S"] = m["Income"] - m["Expense"]
    y = m["S"].values
    if len(y) < 2: return [float(y[-1])] * ahead
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    return [round(slope*(len(y)+i)+intercept, 2) for i in range(ahead)]

def page_header(title, sub=""):
    st.markdown(f'<div class="fv-page-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="fv-page-sub">{sub}</div>', unsafe_allow_html=True)

def glass_kpi(label, value, color=GREEN, pill_class="kpi-pill-green", tag=""):
    tag_html = f'<div class="kpi-pill {pill_class}">{tag}</div>' if tag else ""
    return f"""<div class="glass-card" style="padding:1rem 1.3rem;">
        {tag_html}
        <div class="kpi-label-sm">{label}</div>
        <div class="kpi-big" style="color:{color};">{value}</div>
    </div>"""

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">FinVault</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">// AI BUDGET PLANNER</div>', unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(f'<div class="user-badge">◉ &nbsp;{st.session_state.username}</div>',
                    unsafe_allow_html=True)
        nav_pages = [
            "📊 Dashboard", "➕ Add Transaction", "🔄 Recurring",
            "🔎 Search & Filter", "💰 Budget Planner", "⭐ Health Score",
            "📈 Investment Advisor", "🏦 Loan & EMI",
            "🎯 Goals", "🏆 Achievements", "📅 Bills", "📸 Scan Receipt",
            "📄 Export Reports", "✏️ Edit / Delete",
        ]
        menu = st.radio("", nav_pages, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⏻  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = ""
            st.rerun()
    else:
        menu = st.radio("", ["🏠 Home", "🔐 Login", "📝 Signup"], label_visibility="collapsed")

# ─────────────────────────────────────────
# ── HOME ──
# ─────────────────────────────────────────
if menu == "🏠 Home":
    st.markdown("<br>", unsafe_allow_html=True)
    page_header("FinVault 💰", "// your money. visualised. dominated.")

    features = [
        ("📊", "Real-time dashboard with animated charts"),
        ("🔄", "Recurring transactions tracking"),
        ("💰", "Monthly budget planner with alerts"),
        ("⭐", "AI financial health score (0–100)"),
        ("🤖", "ML savings forecast for next 3 months"),
        ("📈", "Personalised investment advisor"),
        ("🏦", "Loan & EMI calculator with amortisation"),
        ("💱", "Multi-currency support (16 currencies)"),
        ("📄", "Export reports to CSV"),
    ]
    cols = st.columns(2)
    for i, (icon, text) in enumerate(features):
        cols[i % 2].markdown(
            f'<div class="home-feature"><span>{icon}</span>{text}</div>',
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="fv-page-sub" style="text-align:center;">← login or signup from the sidebar to get started</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────
# ── SIGNUP ──
# ─────────────────────────────────────────
elif menu == "📝 Signup":
    st.markdown("<br>", unsafe_allow_html=True)
    page_header("Create account", "// join finvault")
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="e.g. Soham")
        email    = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="min 4 characters")
        sub = st.form_submit_button("Create account →", use_container_width=True)
    if sub:
        if not username or not email or not password:
            st.warning("Fill in all fields.")
        else:
            try:
                existing = sb_select("users", {"email": f"eq.{email}", "select": "user_id"})
                if existing:
                    st.error("Email already registered.")
                else:
                    sb_insert("users", {"username": username, "email": email, "password": password})
                    st.success("Account created! Login now.")
            except Exception as e:
                st.error(f"Error: {e}")

# ─────────────────────────────────────────
# ── LOGIN ──
# ─────────────────────────────────────────
elif menu == "🔐 Login":
    st.markdown("<br>", unsafe_allow_html=True)
    page_header("Login", "// welcome back")
    st.markdown('''<div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.18);
        border-radius:12px;padding:10px 16px;font-family:'DM Mono',monospace;font-size:0.78rem;
        color:#00e5a0;margin-bottom:1rem;">
        First time here? Go to <b>Signup</b> in the sidebar to create your account first.
    </div>''', unsafe_allow_html=True)
    with st.form("login_form"):
        email    = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="your password")
        sub = st.form_submit_button("Login →", use_container_width=True)
    if sub:
        res = sb_select("users", {"email": f"eq.{email}", "password": f"eq.{password}"})
        user = res[0] if res else None
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id   = user["user_id"]
            st.session_state.username  = user["username"]
            st.success(f"Welcome back, {user['username']}!")
            st.rerun()
        else:
            st.error("Invalid credentials. New user? Click Signup in the sidebar.")

elif not st.session_state.logged_in:
    st.warning("Login first.")

# ─────────────────────────────────────────
# ── DASHBOARD ──
# ─────────────────────────────────────────
elif menu == "📊 Dashboard":
    df = load_transactions(st.session_state.user_id)
    _hour = datetime.now().hour
    _greet = "Good Morning" if 5 <= _hour < 12 else "Good Afternoon" if 12 <= _hour < 17 else "Good Evening" if 17 <= _hour < 21 else "Good Night"
    _greet_icon = "☀️" if 5 <= _hour < 12 else "🌤️" if 12 <= _hour < 17 else "🌙" if 17 <= _hour < 21 else "🌑"
    page_header(f"{_greet}, {st.session_state.username}! {_greet_icon}", f"// {datetime.today().strftime('%A, %d %B %Y')}  ·  your financial pulse")

    if df.empty:
        st.info("No transactions yet — add your first one.")
        st.stop()

    total_inc  = df[df["Type"]=="Income"]["Amount_INR"].sum()
    total_exp  = df[df["Type"]=="Expense"]["Amount_INR"].sum()
    savings    = total_inc - total_exp
    score, _   = compute_health_score(df)
    score_color = GREEN if score >= 70 else (GOLD if score >= 40 else RED)

    # ── Ticker bar ──
    _ticker_items = [
        f"INCOME  ₹{total_inc:,.0f}",
        f"EXPENSES  ₹{total_exp:,.0f}",
        f"SAVINGS  ₹{savings:,.0f}",
        f"HEALTH SCORE  {score}/100",
        f"TRANSACTIONS  {len(df)}",
        f"DATE  {datetime.today().strftime('%d %b %Y')}",
        f"CATEGORIES  {df['Category'].nunique()}",
    ]
    _ticker_str = "     ●     ".join(_ticker_items) + "     ●     " + "     ●     ".join(_ticker_items)
    st.markdown(f'''<div class="fv-ticker-wrap">
        <span class="fv-ticker">{_ticker_str}</span>
    </div>''', unsafe_allow_html=True)

    # ── Hero greeting card ──
    _savings_pct = (savings/total_inc*100) if total_inc > 0 else 0
    _months = df["Date"].dt.to_period("M").nunique()
    st.markdown(f'''<div class="fv-hero">
        <div class="fv-hero-greeting">{_greet}, {st.session_state.username}! {_greet_icon}</div>
        <div class="fv-hero-sub">// {datetime.today().strftime("%A, %d %B %Y")} · your financial pulse</div>
        <div class="fv-hero-stats">
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">₹{total_inc:,.0f}</span>
                <span class="fv-hero-stat-lbl">Total Income</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val" style="color:#ff6060;">₹{total_exp:,.0f}</span>
                <span class="fv-hero-stat-lbl">Total Spent</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val" style="color:#c8a800;">₹{savings:,.0f}</span>
                <span class="fv-hero-stat-lbl">Net Saved</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val" style="color:{score_color};">{score}/100</span>
                <span class="fv-hero-stat-lbl">Health Score</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val" style="color:#00d2ff;">{_savings_pct:.1f}%</span>
                <span class="fv-hero-stat-lbl">Savings Rate</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">{_months}</span>
                <span class="fv-hero-stat-lbl">Months Active</span>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)

    # ── KPI cards with sparklines ──
    _spark_df = df.copy()
    _spark_df["Month"] = _spark_df["Date"].dt.to_period("M").astype(str)
    _monthly_inc = _spark_df[_spark_df["Type"]=="Income"].groupby("Month")["Amount_INR"].sum().reset_index()
    _monthly_exp = _spark_df[_spark_df["Type"]=="Expense"].groupby("Month")["Amount_INR"].sum().reset_index()
    _monthly_sav = _monthly_inc.set_index("Month").join(
        _monthly_exp.set_index("Month"), lsuffix="_i", rsuffix="_e"
    ).fillna(0)
    _monthly_sav["sav"] = _monthly_sav.get("Amount_INR_i", 0) - _monthly_sav.get("Amount_INR_e", 0)

    def _mini_spark(values, color, height=40):
        if len(values) < 2: return ""
        import json
        vals = [float(v) for v in values]
        mn, mx = min(vals), max(vals)
        rng = mx - mn or 1
        pts = [(i/(len(vals)-1))*100 for i in range(len(vals))]
        ys  = [height - ((v-mn)/rng)*(height-4) - 2 for v in vals]
        path = " ".join([f"{'M' if i==0 else 'L'}{x:.1f},{y:.1f}" for i,(x,y) in enumerate(zip(pts,ys))])
        fill_pts = f"M0,{height} " + path[1:] + f" L100,{height} Z"
        return f'''<svg viewBox="0 0 100 {height}" width="100%" height="{height}"
            preserveAspectRatio="none" style="display:block;margin-top:4px;">
            <defs><linearGradient id="sg{color[1:]}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{color}" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="{color}" stop-opacity="0.02"/>
            </linearGradient></defs>
            <path d="{fill_pts}" fill="url(#sg{color[1:]})" />
            <path d="{path}" fill="none" stroke="{color}" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round"/>
        </svg>'''

    _inc_spark = _mini_spark(_monthly_inc["Amount_INR"].tolist(), "#00e5a0")
    _exp_spark = _mini_spark(_monthly_exp["Amount_INR"].tolist(), "#ff6060")
    _sav_spark = _mini_spark(_monthly_sav["sav"].tolist() if not _monthly_sav.empty else [], "#c8a800")
    _score_history = [score]  # single point placeholder

    st.markdown(f'''<div class="fv-kpi-grid">
        <div class="fv-kpi-card fv-kpi-income">
            <div class="fv-kpi-tag" style="background:rgba(0,229,160,0.1);color:#00e5a0;border:1px solid rgba(0,229,160,0.22);">INCOME</div>
            <div class="fv-kpi-val" style="color:#00e5a0;">₹{total_inc:,.0f}</div>
            <div class="fv-kpi-label">total income</div>
            <div class="fv-sparkline">{_inc_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-expense">
            <div class="fv-kpi-tag" style="background:rgba(255,96,96,0.1);color:#ff6060;border:1px solid rgba(255,96,96,0.22);">EXPENSE</div>
            <div class="fv-kpi-val" style="color:#ff6060;">₹{total_exp:,.0f}</div>
            <div class="fv-kpi-label">total spent</div>
            <div class="fv-sparkline">{_exp_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-savings">
            <div class="fv-kpi-tag" style="background:rgba(200,168,0,0.1);color:#c8a800;border:1px solid rgba(200,168,0,0.22);">SAVINGS</div>
            <div class="fv-kpi-val" style="color:#c8a800;">₹{savings:,.0f}</div>
            <div class="fv-kpi-label">net saved</div>
            <div class="fv-sparkline">{_sav_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-score">
            <div class="fv-kpi-tag" style="background:rgba(0,210,255,0.1);color:#00d2ff;border:1px solid rgba(0,210,255,0.22);">SCORE</div>
            <div class="fv-kpi-val" style="color:{score_color};">{score}<span style="font-size:1rem;color:#555;">/100</span></div>
            <div class="fv-kpi-label">health score</div>
        </div>
    </div>''', unsafe_allow_html=True)

    expense_df = df[df["Type"]=="Expense"]
    income_df  = df[df["Type"]=="Income"]

    # ── Helper: format month labels properly ──
    def fmt_months(df_in):
        d = df_in.copy()
        d["Month"] = d["Date"].dt.strftime("%b %Y")   # "May 2026"
        d["MonthSort"] = d["Date"].dt.to_period("M").astype(str)
        return d

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════
    # ROW 1 — Animated Donut + Gradient Bar
    # ══════════════════════════════════════
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="fv-chart-card">', unsafe_allow_html=True)
        st.markdown("""<div class="section-tag">BREAKDOWN</div>
        <div class="fv-section-title">where the bag goes</div>""", unsafe_allow_html=True)
        if not expense_df.empty:
            cat_exp = expense_df.groupby("Category")["Amount_INR"].sum().reset_index().sort_values("Amount_INR", ascending=False)
            NEON_PAL = ["#00e5a0","#c8a800","#ff6060","#00d2ff","#a855f7","#fb923c","#f472b6","#34d399"]
            fig_donut = go.Figure()
            fig_donut.add_trace(go.Pie(
                labels=cat_exp["Category"],
                values=cat_exp["Amount_INR"],
                hole=0.68,
                marker=dict(
                    colors=NEON_PAL[:len(cat_exp)],
                    line=dict(color="#080808", width=4)
                ),
                textinfo="label+percent",
                textfont=dict(size=10, color="#e8e8e8", family="DM Mono"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
                direction="clockwise",
                rotation=90,
            ))
            # Centre annotation
            fig_donut.add_annotation(
                text=f"<b>₹{total_exp:,.0f}</b><br><span style='font-size:9px'>total spent</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=12, color="#ff6060", family="DM Mono"),
                xref="paper", yref="paper", align="center"
            )
            _donut_layout = plotly_base(320)
            _donut_layout.update(dict(
                showlegend=True,
                legend=dict(
                    bgcolor="rgba(0,0,0,0)", font=dict(size=10, family="DM Mono"),
                    orientation="v", x=1.02, y=0.5, yanchor="middle"
                ),
            ))
            fig_donut.update_layout(**_donut_layout)
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""<div style="height:200px;display:flex;flex-direction:column;
                align-items:center;justify-content:center;border:1px dashed rgba(0,229,160,0.12);
                border-radius:16px;color:#333;font-family:'DM Mono',monospace;font-size:0.8rem;">
                <div style="font-size:2rem;margin-bottom:8px;">💸</div>
                no expense data yet<br>add transactions to see breakdown
            </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown("""<div class="section-tag">MONTHLY</div>
        <div class="fv-section-title">income vs expense 📊</div>""", unsafe_allow_html=True)

        df2 = fmt_months(df)
        # Keep sort order
        month_order = df2.sort_values("MonthSort")["Month"].unique().tolist()
        monthly_raw = df2.groupby(["Month","MonthSort","Type"])["Amount_INR"].sum().reset_index()
        monthly_raw = monthly_raw.sort_values("MonthSort")
        monthly = monthly_raw.pivot_table(index=["Month","MonthSort"], columns="Type", values="Amount_INR", fill_value=0).reset_index()
        monthly = monthly.sort_values("MonthSort")

        inc_vals = monthly["Income"].tolist()  if "Income"  in monthly.columns else [0]*len(monthly)
        exp_vals = monthly["Expense"].tolist() if "Expense" in monthly.columns else [0]*len(monthly)
        x_labels = monthly["Month"].tolist()

        fig_bar = go.Figure()
        # Income — gradient green bars
        fig_bar.add_trace(go.Bar(
            name="💚 Income", x=x_labels, y=inc_vals,
            marker=dict(
                color=inc_vals,
                colorscale=[[0,"#005c40"],[0.5,"#00b37a"],[1,"#00e5a0"]],
                showscale=False, line_width=0,
                cornerradius=6,
            ),
            hovertemplate="<b>%{x}</b><br>Income: ₹%{y:,.0f}<extra></extra>",
            width=0.35,
        ))
        # Expense — gradient red bars
        fig_bar.add_trace(go.Bar(
            name="🔴 Expense", x=x_labels, y=exp_vals,
            marker=dict(
                color=exp_vals,
                colorscale=[[0,"#4a0000"],[0.5,"#cc2200"],[1,"#ff6060"]],
                showscale=False, line_width=0,
                cornerradius=6,
            ),
            hovertemplate="<b>%{x}</b><br>Expense: ₹%{y:,.0f}<extra></extra>",
            width=0.35,
        ))
        # Net savings line on top
        net_vals = [i - e for i, e in zip(inc_vals, exp_vals)]
        fig_bar.add_trace(go.Scatter(
            name="✨ Net", x=x_labels, y=net_vals,
            mode="lines+markers",
            line=dict(color=GOLD, width=2, dash="dot"),
            marker=dict(size=7, color=GOLD, line=dict(color=BG, width=1)),
            hovertemplate="<b>%{x}</b><br>Net: ₹%{y:,.0f}<extra></extra>",
            yaxis="y",
        ))
        lay = plotly_base(320)
        lay.update(
            barmode="group", bargap=0.28, bargroupgap=0.06,
            xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                       tickfont=dict(size=10, family="DM Mono"), tickangle=-25,
                       categoryorder="array", categoryarray=x_labels),
            yaxis=dict(gridcolor=GRID, showline=False, zeroline=True,
                       zerolinecolor="rgba(255,255,255,0.08)",
                       tickprefix="₹", tickfont=dict(size=9, family="DM Mono")),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), orientation="h",
                        y=-0.22, x=0.5, xanchor="center"),
            shapes=[dict(
                type="rect", xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color="rgba(0,229,160,0.06)", width=1),
                layer="below"
            )]
        )
        fig_bar.update_layout(**lay)
        if not x_labels:
            st.markdown("""<div style="height:200px;display:flex;align-items:center;
                justify-content:center;border:1px dashed rgba(0,229,160,0.12);
                border-radius:16px;color:#333;font-family:'DM Mono',monospace;font-size:0.8rem;">
                no data yet</div>""", unsafe_allow_html=True)
        else:
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════
    # ROW 2 — Full-width Glow Area + Scatter
    # ══════════════════════════════════════
    st.markdown("""<div class="section-tag">VIBE CHECK</div>
    <div class="fv-section-title">spending wave 🌊</div>""", unsafe_allow_html=True)

    df3 = fmt_months(df)
    # Daily totals for a more interesting wave
    df3["DayStr"] = df3["Date"].dt.strftime("%d %b")
    df3["DateOnly"] = df3["Date"].dt.date
    daily_exp = df3[df3["Type"]=="Expense"].groupby("DateOnly")["Amount_INR"].sum().reset_index()
    daily_inc = df3[df3["Type"]=="Income"].groupby("DateOnly")["Amount_INR"].sum().reset_index()

    if not daily_exp.empty or not daily_inc.empty:
        fig_wave = go.Figure()

        if not daily_inc.empty:
            # Income glow layers
            for op, w in [(0.04, 24), (0.1, 10), (0.22, 4), (1.0, 2)]:
                fig_wave.add_trace(go.Scatter(
                    x=daily_inc["DateOnly"].astype(str), y=daily_inc["Amount_INR"],
                    mode="lines",
                    line=dict(color=GREEN, width=w),
                    fill="tozeroy" if op==0.04 else "none",
                    fillcolor="rgba(0,229,160,0.03)",
                    opacity=op, showlegend=False,
                    hoverinfo="skip" if op < 1 else "all",
                    hovertemplate="<b>%{x}</b><br>Income ₹%{y:,.0f}<extra></extra>" if op==1 else None,
                ))
            fig_wave.add_trace(go.Scatter(
                x=daily_inc["DateOnly"].astype(str), y=daily_inc["Amount_INR"],
                mode="markers", name="💚 Income",
                marker=dict(size=8, color=GREEN,
                            line=dict(color=BG, width=1.5),
                            symbol="circle"),
                hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra>Income</extra>",
            ))

        if not daily_exp.empty:
            # Expense glow layers
            for op, w in [(0.04, 24), (0.1, 10), (0.22, 4), (1.0, 2)]:
                fig_wave.add_trace(go.Scatter(
                    x=daily_exp["DateOnly"].astype(str), y=[-v for v in daily_exp["Amount_INR"]],
                    mode="lines",
                    line=dict(color=RED, width=w),
                    fill="tozeroy" if op==0.04 else "none",
                    fillcolor="rgba(255,96,96,0.03)",
                    opacity=op, showlegend=False,
                    hoverinfo="skip" if op < 1 else "all",
                    hovertemplate="<b>%{x}</b><br>Expense ₹%{y:,.0f}<extra></extra>" if op==1 else None,
                ))
            fig_wave.add_trace(go.Scatter(
                x=daily_exp["DateOnly"].astype(str),
                y=[-v for v in daily_exp["Amount_INR"]],
                mode="markers", name="🔴 Expense",
                marker=dict(size=8, color=RED,
                            line=dict(color=BG, width=1.5),
                            symbol="diamond"),
                hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra>Expense</extra>",
            ))

        # Zero line
        fig_wave.add_hline(y=0, line_color="rgba(255,255,255,0.1)", line_width=1)
        lay2 = plotly_base(300)
        lay2.update(
            xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                       tickfont=dict(size=9, family="DM Mono"), tickangle=-30,
                       nticks=8),
            yaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                       tickprefix="₹", tickfont=dict(size=9, family="DM Mono")),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), orientation="h",
                        y=-0.22, x=0.5, xanchor="center"),
        )
        fig_wave.update_layout(**lay2)
        st.plotly_chart(fig_wave, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("""<div style="height:160px;display:flex;align-items:center;
            justify-content:center;border:1px dashed rgba(0,229,160,0.12);
            border-radius:16px;color:#333;font-family:'DM Mono',monospace;font-size:0.8rem;">
            🌊 add transactions to see your spending wave</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════
    # ROW 3 — Category Heatmap-style + Forecast
    # ══════════════════════════════════════
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""<div class="section-tag">CATEGORY RANK</div>
        <div class="fv-section-title">top spending categories 🏆</div>""", unsafe_allow_html=True)
        if not expense_df.empty:
            top_cats = expense_df.groupby("Category")["Amount_INR"].sum().sort_values(ascending=True).reset_index()
            # Colour by rank
            n = len(top_cats)
            bar_colors_rank = []
            for i in range(n):
                ratio = i / max(n-1, 1)
                bar_colors_rank.append(f"rgba({int(255*ratio)},{int(229*(1-ratio)+160*ratio)},{int(160*(1-ratio))},0.85)")

            fig_rank = go.Figure(go.Bar(
                x=top_cats["Amount_INR"], y=top_cats["Category"],
                orientation="h",
                marker=dict(
                    color=bar_colors_rank,
                    line_width=0,
                    cornerradius=6,
                ),
                text=[f"₹{v:,.0f}" for v in top_cats["Amount_INR"]],
                textposition="outside",
                textfont=dict(size=10, color=FONT_C, family="DM Mono"),
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            ))
            lay3 = plotly_base(max(220, n*45))
            lay3.update(
                xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                           tickprefix="₹", tickfont=dict(size=9)),
                yaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                           tickfont=dict(size=10, family="DM Mono")),
                margin=dict(l=10, r=60, t=20, b=10),
            )
            fig_rank.update_layout(**lay3)
            st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""<div style="height:180px;display:flex;align-items:center;
                justify-content:center;border:1px dashed rgba(0,229,160,0.12);
                border-radius:16px;color:#333;font-family:'DM Mono',monospace;font-size:0.8rem;">
                🏆 no categories yet</div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""<div class="section-tag">AI FORECAST</div>
        <div class="fv-section-title">predicted savings 🔮</div>""", unsafe_allow_html=True)
        preds = predict_savings(df, ahead=3)
        if preds:
            dp = df.copy(); dp["Month"] = dp["Date"].dt.to_period("M")
            ms = dp.groupby(["Month","Type"])["Amount_INR"].sum().unstack(fill_value=0)
            ms["Savings"] = ms.get("Income", pd.Series(dtype=float)) if "Income" in ms.columns else 0
            if "Income" in ms.columns and "Expense" in ms.columns:
                ms["Savings"] = ms["Income"] - ms["Expense"]
            elif "Income" in ms.columns:
                ms["Savings"] = ms["Income"]
            else:
                ms["Savings"] = 0
            lp_raw = ms.index.tolist()
            lp     = [p.strftime("%b %Y") for p in lp_raw]
            ls     = ms["Savings"].tolist()
            lp_last = lp_raw[-1]
            fl     = [(lp_last + i).strftime("%b %Y") for i in range(1, 4)]

            fig_fc = go.Figure()
            bar_colors_fc = [GREEN if v >= 0 else RED for v in ls]
            fig_fc.add_trace(go.Bar(
                x=lp, y=ls, name="actual",
                marker=dict(color=bar_colors_fc, line_width=0, cornerradius=6),
                hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra>Actual</extra>",
            ))
            fig_fc.add_trace(go.Bar(
                x=fl, y=preds, name="predicted 🔮",
                marker=dict(
                    color=GOLD, opacity=0.7,
                    pattern=dict(shape="/", fgcolor=GREEN, size=6),
                    line=dict(color=GOLD, width=1.5),
                    cornerradius=6,
                ),
                hovertemplate="<b>%{x} (AI)</b><br>₹%{y:,.0f}<extra>Predicted</extra>",
            ))
            lay4 = plotly_base(max(220, len(lp)*40))
            lay4.update(
                barmode="group", bargap=0.3,
                xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                           tickfont=dict(size=9, family="DM Mono"), tickangle=-30,
                           categoryorder="array", categoryarray=lp+fl),
                yaxis=dict(gridcolor=GRID, showline=False, zeroline=True,
                           zerolinecolor="rgba(255,255,255,0.08)",
                           tickprefix="₹", tickfont=dict(size=9)),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), orientation="h",
                            y=-0.26, x=0.5, xanchor="center"),
            )
            fig_fc.update_layout(**lay4)
            st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""<div style="height:180px;display:flex;flex-direction:column;
                align-items:center;justify-content:center;border:1px dashed rgba(0,229,160,0.12);
                border-radius:16px;color:#333;font-family:'DM Mono',monospace;font-size:0.8rem;gap:8px;">
                <div style="font-size:1.8rem;">🔮</div>
                add transactions across multiple months<br>to unlock AI savings forecast
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ── ADD TRANSACTION ──
# ─────────────────────────────────────────
elif menu == "➕ Add Transaction":
    page_header("Add Transaction", "// log your money moves")
    with st.form("add_tx"):
        col1, col2 = st.columns(2)
        tx_type  = col1.selectbox("Type", ["Income","Expense"])
        category = col2.text_input("Category  (e.g. Salary, Food, Rent)")
        col3, col4 = st.columns([2,1])
        amount   = col3.number_input("Amount", min_value=0.01, step=0.01)
        currency = col4.selectbox("Currency", list(CURRENCY_RATES.keys()))
        rate        = CURRENCY_RATES[currency]
        amount_inr  = amount * rate
        cur_code    = currency.split()[0]
        tx_date     = st.date_input("Date", value=date.today())
        description = st.text_area("Note (optional)", height=80)
        col5, col6 = st.columns([1,2])
        is_rec   = col5.checkbox("🔄 Recurring")
        rec_freq = col6.selectbox("Frequency", ["Monthly","Weekly","Yearly"]) if is_rec else ""
        submitted = st.form_submit_button("Log transaction →", use_container_width=True)

    if submitted:
        if not category:
            st.warning("Enter a category.")
        else:
            sb_insert("transactions", {
                "user_id": st.session_state.user_id, "type": tx_type,
                "category": category, "amount": amount, "date": str(tx_date),
                "description": description, "is_recurring": int(is_rec),
                "recur_freq": rec_freq, "currency": cur_code, "amount_inr": amount_inr
            })
            st.success(f"✅ Logged — {amount:,.2f} {cur_code} = ₹{amount_inr:,.2f}")
            if cur_code != "INR":
                st.caption(f"Rate used: 1 {cur_code} = ₹{rate}")

# ─────────────────────────────────────────
# ── RECURRING ──
# ─────────────────────────────────────────
elif menu == "🔄 Recurring":
    page_header("Recurring Transactions", "// set it and forget it")
    df = load_transactions(st.session_state.user_id)
    recurring = df[df["Recurring"]==1] if not df.empty else pd.DataFrame()

    if recurring.empty:
        st.info("No recurring transactions. Check '🔄 Recurring' when adding a transaction.")
        st.stop()

    st.markdown(f'<div class="fv-page-sub">// {len(recurring)} active recurring entries</div>', unsafe_allow_html=True)
    for _, row in recurring.iterrows():
        color = GREEN if row["Type"]=="Income" else RED
        st.markdown(f"""<div class="glass-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:700;color:#e8e8e8;font-size:0.95rem;">{row['Category']}</div>
                    <div style="font-size:0.75rem;color:#555;font-family:'DM Mono',monospace;">
                        {row['Type']} · {row['Frequency']} · last: {row['Date'].strftime('%Y-%m-%d')}</div>
                </div>
                <div style="font-family:'DM Mono',monospace;font-size:1.2rem;font-weight:600;color:{color};">
                    ₹{row['Amount']:,.0f}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Log again today", key=f"rl_{row['ID']}"):
            sb_insert("transactions", {
                "user_id": st.session_state.user_id, "type": row["Type"],
                "category": row["Category"], "amount": float(row["Amount"]),
                "date": str(date.today()), "description": row["Description"],
                "is_recurring": 1, "recur_freq": row["Frequency"],
                "currency": "INR", "amount_inr": float(row["Amount"])
            })
            st.success(f"Logged {row['Category']}!")
            st.rerun()

    st.divider()
    st.markdown('<div class="fv-section-title">this month status</div>', unsafe_allow_html=True)
    month_str = date.today().strftime("%Y-%m")
    if not df.empty:
        df2 = df.copy(); df2["M"] = df2["Date"].dt.strftime("%Y-%m")
        logged_cats = df2[df2["M"]==month_str]["Category"].tolist()
    else:
        logged_cats = []
    for _, row in recurring.iterrows():
        done = row["Category"] in logged_cats
        badge = f'<span class="kpi-pill kpi-pill-green">✓ logged</span>' if done else \
                f'<span class="kpi-pill kpi-pill-gold">⏳ pending</span>'
        st.markdown(f'<div style="padding:6px 0;font-size:0.88rem;color:#aaa;">'
                    f'{badge} &nbsp;<b style="color:#e8e8e8">{row["Category"]}</b> '
                    f'· ₹{row["Amount"]:,.0f} · {row["Frequency"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# ── SEARCH & FILTER ──
# ─────────────────────────────────────────
elif menu == "🔎 Search & Filter":
    page_header("Search & Filter", "// find any transaction")
    df = load_transactions(st.session_state.user_id)
    if df.empty:
        st.info("No transactions found.")
        st.stop()

    with st.expander("⚙️ Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        kw      = c1.text_input("Keyword")
        tf      = c2.selectbox("Type", ["All","Income","Expense"])
        cats    = ["All"] + sorted(df["Category"].unique().tolist())
        cf      = c3.selectbox("Category", cats)
        c4, c5  = st.columns(2)
        d_from  = c4.date_input("From", value=df["Date"].min().date())
        d_to    = c5.date_input("To",   value=df["Date"].max().date())

    fil = df.copy()
    if kw:
        fil = fil[fil["Category"].str.contains(kw, case=False, na=False) |
                  fil["Description"].str.contains(kw, case=False, na=False)]
    if tf != "All": fil = fil[fil["Type"]==tf]
    if cf != "All": fil = fil[fil["Category"]==cf]
    fil = fil[(fil["Date"].dt.date >= d_from) & (fil["Date"].dt.date <= d_to)]

    st.markdown(f'<div class="fv-page-sub">// {len(fil)} of {len(df)} transactions</div>', unsafe_allow_html=True)

    if not fil.empty:
        disp = fil.copy(); disp["Date"] = disp["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(disp[["ID","Type","Category","Amount","Currency","Date","Description"]],
                     use_container_width=True, hide_index=True)
        inc = fil[fil["Type"]=="Income"]["Amount_INR"].sum()
        exp = fil[fil["Type"]=="Expense"]["Amount_INR"].sum()
        c1,c2,c3 = st.columns(3)
        c1.metric("Income", f"₹{inc:,.0f}")
        c2.metric("Expense", f"₹{exp:,.0f}")
        c3.metric("Net", f"₹{inc-exp:,.0f}")
    else:
        st.warning("Nothing matches.")

# ─────────────────────────────────────────
# ── BUDGET PLANNER ──
# ─────────────────────────────────────────
elif menu == "💰 Budget Planner":
    page_header("Budget Planner", "// set limits. stay in range.")
    month_str = st.text_input("Month (YYYY-MM)", value=datetime.today().strftime("%Y-%m"))
    df = load_transactions(st.session_state.user_id)

    col1, col2, col3 = st.columns([2,2,1])
    new_cat = col1.text_input("Category")
    new_amt = col2.number_input("Budget (₹)", min_value=0.0, step=100.0)
    col3.markdown("<br>", unsafe_allow_html=True)
    if col3.button("Save", use_container_width=True):
        if not new_cat.strip():
            st.warning("Enter a category.")
        else:
            sb_upsert("budgets", {
                "user_id": st.session_state.user_id,
                "category": new_cat.strip(),
                "month": month_str,
                "amount": new_amt
            }, on_conflict="user_id,category,month")
            st.success(f"Saved budget for {new_cat}!")

    budgets = load_budgets(st.session_state.user_id, month_str)
    if not budgets:
        st.info("No budgets for this month. Add categories above.")
    else:
        if not df.empty:
            df3 = df.copy(); df3["M"] = df3["Date"].dt.strftime("%Y-%m")
            me = df3[(df3["M"]==month_str) & (df3["Type"]=="Expense")]
            actual = me.groupby("Category")["Amount_INR"].sum().to_dict()
        else:
            actual = {}

        tb = sum(budgets.values())
        ts = sum(actual.get(c,0) for c in budgets)
        delta = tb - ts
        c1,c2,c3 = st.columns(3)
        c1.metric("Budget", f"₹{tb:,.0f}")
        c2.metric("Spent", f"₹{ts:,.0f}")
        c3.metric("Remaining", f"₹{abs(delta):,.0f}", delta=f"{'Under' if delta>=0 else 'Over'}")

        st.markdown("<br>", unsafe_allow_html=True)
        for cat, budget_amt in budgets.items():
            spent = actual.get(cat, 0)
            pct   = min(100, (spent/budget_amt*100) if budget_amt > 0 else 0)
            over  = spent > budget_amt
            warn  = pct > 80 and not over
            fill_color = f"linear-gradient(90deg, {RED},{RED})" if over else \
                         f"linear-gradient(90deg, {GOLD},{GOLD})" if warn else \
                         f"linear-gradient(90deg, {GREEN},{GOLD})"
            status = '<span class="kpi-pill kpi-pill-red">OVER</span>' if over else \
                     '<span class="kpi-pill kpi-pill-gold">WARNING</span>' if warn else \
                     '<span class="kpi-pill kpi-pill-green">OK</span>'
            st.markdown(f"""<div style="margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:600;color:#e8e8e8;font-size:0.9rem;">{cat}</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.8rem;color:#888;">
                    ₹{spent:,.0f} / ₹{budget_amt:,.0f} &nbsp;{status}</span>
            </div>
            <div class="budget-bar-bg"><div class="budget-bar-fill" style="width:{pct}%;background:{fill_color};"></div></div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# ── HEALTH SCORE ──
# ─────────────────────────────────────────
elif menu == "⭐ Health Score":
    page_header("Health Score", "// how healthy is your wallet?")
    df = load_transactions(st.session_state.user_id)
    score, components = compute_health_score(df)
    if score == 0:
        st.info("Add more transactions to generate your score.")
        st.stop()

    score_color = GREEN if score >= 70 else (GOLD if score >= 40 else RED)
    grade = "EXCELLENT" if score>=85 else "GOOD" if score>=70 else "FAIR" if score>=50 else "NEEDS WORK"

    col_g, col_d = st.columns([1,2])
    with col_g:
        # Plotly gauge
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number=dict(font=dict(family="DM Mono", size=44, color=score_color)),
            gauge=dict(
                axis=dict(range=[0,100], tickwidth=0, tickcolor=BG,
                          tickfont=dict(color="#555", size=9)),
                bar=dict(color=score_color, thickness=0.28),
                bgcolor=PLOT_BG,
                borderwidth=0,
                steps=[
                    dict(range=[0,40],  color="rgba(255,80,80,0.08)"),
                    dict(range=[40,70], color="rgba(200,168,0,0.08)"),
                    dict(range=[70,100],color="rgba(57,255,20,0.08)"),
                ],
                threshold=dict(line=dict(color=score_color, width=3), thickness=0.8, value=score)
            )
        ))
        fig_g.update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
                            margin=dict(l=10,r=10,t=20,b=10), height=240,
                            font=dict(family="DM Mono", color=FONT_C))
        st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f'<div style="text-align:center;"><span class="kpi-pill kpi-pill-green">{grade}</span></div>',
                    unsafe_allow_html=True)

    with col_d:
        st.markdown("<br>", unsafe_allow_html=True)
        for comp, val in components.items():
            pct = val / 25
            fill = GREEN if pct > 0.7 else (GOLD if pct > 0.4 else RED)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-size:0.82rem;color:#aaa;">{comp}</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.82rem;color:{fill};">{val}/25</span>
            </div>
            <div class="budget-bar-bg"><div class="budget-bar-fill" style="width:{pct*100:.0f}%;background:{fill};"></div></div>
            """, unsafe_allow_html=True)

    st.divider()
    inc = df[df["Type"]=="Income"]["Amount_INR"].sum()
    exp = df[df["Type"]=="Expense"]["Amount_INR"].sum()
    sr  = ((inc-exp)/inc*100) if inc > 0 else 0
    st.markdown('<div class="fv-section-title">💡 AI tips</div>', unsafe_allow_html=True)
    if sr < 20:
        st.warning(f"Savings rate is {sr:.1f}% — below 20%. Cut discretionary spend to improve.")
    elif sr >= 40:
        st.success(f"Savings rate is {sr:.1f}% — excellent! Invest that surplus.")
    if components.get("Income diversity",0) < 15:
        st.info("Diversify income sources (freelance, dividends) to boost your score.")
    if components.get("Consistency",0) < 15:
        st.info("Log transactions every month to unlock consistency points.")

# ─────────────────────────────────────────
# ── INVESTMENT ADVISOR ──
# ─────────────────────────────────────────
elif menu == "📈 Investment Advisor":
    page_header("Investment Advisor", "// grow your bag")
    df = load_transactions(st.session_state.user_id)
    inc = df[df["Type"]=="Income"]["Amount_INR"].sum() if not df.empty else 0
    exp = df[df["Type"]=="Expense"]["Amount_INR"].sum() if not df.empty else 0
    surplus = inc - exp

    c1,c2 = st.columns(2)
    risk    = c1.select_slider("Risk tolerance", ["Low","Medium","High"], value="Medium")
    horizon = c2.selectbox("Horizon", ["< 1 year","1–3 years","3–7 years","7+ years"])
    invest  = st.number_input("Monthly investment (₹)", min_value=0.0,
                               value=max(0.0, round(surplus*0.5, -2)), step=500.0)

    options = {
        "Low": [
            ("🏦 Fixed Deposit",            "6.5–7.5% p.a. · Guaranteed · SBI/HDFC/ICICI",   GREEN),
            ("📜 G-Sec Bonds",              "7–7.5% p.a. · Sovereign guarantee · RBI Direct",  GREEN),
            ("💵 Liquid Mutual Funds",      "6–7% p.a. · High liquidity · Emergency fund",      GREEN),
            ("🏛️ PPF",                     "7.1% p.a. · Tax-free · 80C · 15yr lock-in",        GREEN),
        ],
        "Medium": [
            ("📊 Nifty 50 Index Fund",      "12–14% p.a. historical · Low cost · Broad",        GOLD),
            ("📈 ELSS Mutual Fund",         "12–15% p.a. · 80C benefit · 3yr lock-in",          GOLD),
            ("🏘️ REITs",                   "8–10% yield · Real estate exposure · NSE/BSE",      GOLD),
            ("💰 Balanced Advantage Fund",  "10–12% p.a. · Auto asset allocation",              GOLD),
        ],
        "High": [
            ("📉 Direct Stocks (Nifty 100)","15–20%+ · Requires research · High vol",           RED),
            ("🌐 International ETFs",       "US/Global exposure · Currency diversification",     RED),
            ("💻 Sectoral Funds (IT/Pharma)","High returns in bull markets · Concentration risk",RED),
            ("🪙 Crypto (<5%)",             "Very high risk/reward · Regulatory uncertainty",    "#a855f7"),
        ],
    }
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="fv-section-title">🎯 recommended for you</div>', unsafe_allow_html=True)
    for name, desc, color in options[risk]:
        st.markdown(f"""<div class="invest-card">
            <div class="invest-name" style="color:{color};">{name}</div>
            <div class="invest-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

    if invest > 0:
        st.divider()
        st.markdown('<div class="fv-section-title">📐 SIP growth projection</div>', unsafe_allow_html=True)
        rm = {"Low":0.07,"Medium":0.12,"High":0.15}
        ym = {"< 1 year":1,"1–3 years":3,"3–7 years":7,"7+ years":15}
        r  = rm[risk]/12
        n  = ym[horizon]*12
        fv = invest * (((1+r)**n - 1)/r) * (1+r)
        invested = invest * n
        c1,c2,c3 = st.columns(3)
        c1.metric("Monthly SIP", f"₹{invest:,.0f}")
        c2.metric("Total Invested", f"₹{invested:,.0f}")
        c3.metric(f"Value in {ym[horizon]}y", f"₹{fv:,.0f}")
        months_r = list(range(1, n+1))
        fv_s  = [invest*(((1+r)**m-1)/r)*(1+r) for m in months_r]
        inv_s = [invest*m for m in months_r]
        fig_sip = go.Figure()
        fig_sip.add_trace(go.Scatter(x=months_r, y=fv_s, name="Portfolio value",
                                     line=dict(color=GREEN, width=2),
                                     fill="tozeroy", fillcolor="rgba(57,255,20,0.05)",
                                     hovertemplate="Month %{x}<br>₹%{y:,.0f}<extra>Value</extra>"))
        fig_sip.add_trace(go.Scatter(x=months_r, y=inv_s, name="Invested",
                                     line=dict(color=GOLD, width=1.5, dash="dot"),
                                     hovertemplate="Month %{x}<br>₹%{y:,.0f}<extra>Invested</extra>"))
        fig_sip.update_layout(**plotly_base(300))
        st.plotly_chart(fig_sip, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────
# ── LOAN & EMI ──
# ─────────────────────────────────────────
elif menu == "🏦 Loan & EMI":
    page_header("Loan & EMI Calculator", "// know before you borrow")
    c1,c2,c3 = st.columns(3)
    principal    = c1.number_input("Loan Amount (₹)", min_value=1000.0, value=500000.0, step=10000.0)
    annual_rate  = c2.number_input("Interest Rate (%)", min_value=0.1, max_value=50.0, value=8.5, step=0.1)
    tenure_years = c3.number_input("Tenure (Years)", min_value=1, max_value=30, value=5, step=1)

    r   = annual_rate / 12 / 100
    n   = tenure_years * 12
    emi = principal * r * (1+r)**n / ((1+r)**n - 1)
    tp  = emi * n
    ti  = tp - principal

    c1,c2,c3 = st.columns(3)
    c1.metric("Monthly EMI", f"₹{emi:,.0f}")
    c2.metric("Total Payment", f"₹{tp:,.0f}")
    c3.metric("Total Interest", f"₹{ti:,.0f}")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="fv-section-title">principal vs interest</div>', unsafe_allow_html=True)
        fig_pi = go.Figure(go.Pie(
            labels=["Principal","Interest"],
            values=[principal, ti], hole=0.6,
            marker=dict(colors=[GREEN, RED], line=dict(color=BG, width=3)),
            textinfo="label+percent", textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
        ))
        fig_pi.update_layout(**plotly_base(280), showlegend=False)
        st.plotly_chart(fig_pi, use_container_width=True, config={"displayModeBar": False})

    with col_r:
        st.markdown('<div class="fv-section-title">yearly breakdown</div>', unsafe_allow_html=True)
        bal = principal; sched = []
        for yr in range(1, tenure_years+1):
            yi=yp=0
            for _ in range(12):
                ip = bal*r; pp = emi-ip
                yi+=ip; yp+=pp; bal=max(bal-pp,0)
            sched.append({"Year":yr,"Principal":round(yp,0),"Interest":round(yi,0),"Balance":round(bal,0)})
        st.dataframe(pd.DataFrame(sched), use_container_width=True, hide_index=True)

    st.markdown('<div class="fv-section-title">balance over time</div>', unsafe_allow_html=True)
    bal=principal; bals=[]
    for _ in range(n):
        ip=bal*r; pp=emi-ip; bal=max(bal-pp,0); bals.append(bal)
    fig_bal = go.Figure(go.Scatter(
        x=list(range(1,n+1)), y=bals, mode="lines",
        line=dict(color=GOLD, width=2), fill="tozeroy", fillcolor="rgba(200,168,0,0.06)",
        hovertemplate="Month %{x}<br>₹%{y:,.0f}<extra>Balance</extra>",
    ))
    fig_bal.update_layout(**plotly_base(240))
    st.plotly_chart(fig_bal, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="fv-section-title">compare tenures</div>', unsafe_allow_html=True)
    cmp = []
    for t in [3,5,7,10,15,20]:
        nn=t*12; e=principal*r*(1+r)**nn/((1+r)**nn-1)
        cmp.append({"Tenure (yr)":t,"EMI (₹)":round(e,0),"Total Interest (₹)":round(e*nn-principal,0)})
    st.dataframe(pd.DataFrame(cmp), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────
# ── EXPORT REPORTS ──
# ─────────────────────────────────────────
elif menu == "📄 Export Reports":
    page_header("Export Reports", "// download your data")
    df = load_transactions(st.session_state.user_id)
    if df.empty:
        st.info("No transactions to export.")
        st.stop()

    disp = df.copy(); disp["Date"] = disp["Date"].dt.strftime("%Y-%m-%d")
    buf = io.StringIO(); disp.to_csv(buf, index=False)
    st.download_button("📥 Download all transactions (CSV)", buf.getvalue(),
                       file_name=f"finvault_{st.session_state.username}_all.csv", mime="text/csv")

    st.divider()
    st.markdown('<div class="fv-section-title">filter by month</div>', unsafe_allow_html=True)
    disp2 = df.copy(); disp2["Month"] = disp2["Date"].dt.strftime("%Y-%m")
    months = sorted(disp2["Month"].unique().tolist(), reverse=True)
    sel = st.selectbox("Month", months)
    mdf = disp2[disp2["Month"]==sel].drop(columns=["Month"])
    mdf["Date"] = mdf["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(mdf[["ID","Type","Category","Amount","Currency","Date","Description"]],
                 use_container_width=True, hide_index=True)
    inc = mdf[mdf["Type"]=="Income"]["Amount_INR"].sum()
    exp = mdf[mdf["Type"]=="Expense"]["Amount_INR"].sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("Income", f"₹{inc:,.0f}")
    c2.metric("Expense", f"₹{exp:,.0f}")
    c3.metric("Savings", f"₹{inc-exp:,.0f}")
    buf2 = io.StringIO(); mdf.to_csv(buf2, index=False)
    st.download_button(f"📥 Download {sel} (CSV)", buf2.getvalue(),
                       file_name=f"finvault_{st.session_state.username}_{sel}.csv", mime="text/csv")

# ─────────────────────────────────────────
# ── EDIT / DELETE ──
# ─────────────────────────────────────────
elif menu == "✏️ Edit / Delete":
    page_header("Edit / Delete", "// fix a mistake")
    df = load_transactions(st.session_state.user_id)
    if df.empty:
        st.info("No transactions found.")
        st.stop()

    disp = df.copy(); disp["Date"] = disp["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(disp[["ID","Type","Category","Amount","Currency","Date","Description"]],
                 use_container_width=True, hide_index=True)

    tx_id = st.selectbox("Select Transaction ID", df["ID"].tolist())
    row   = df[df["ID"]==tx_id].iloc[0]

    with st.form("edit_form"):
        c1,c2 = st.columns(2)
        new_type = c1.selectbox("Type", ["Income","Expense"],
                                index=0 if row["Type"]=="Income" else 1)
        new_cat  = c2.text_input("Category", value=row["Category"])
        c3,c4 = st.columns(2)
        new_amt  = c3.number_input("Amount", value=float(row["Amount"]), min_value=0.01)
        new_date = c4.date_input("Date", value=row["Date"].date())
        new_desc = st.text_area("Note", value=row["Description"] or "")
        col_u, col_d = st.columns(2)
        upd = col_u.form_submit_button("💾 Update", use_container_width=True)
        dlt = col_d.form_submit_button("🗑️ Delete", type="secondary", use_container_width=True)

    if upd:
        sb_update("transactions", {
            "type": new_type, "category": new_cat, "amount": new_amt,
            "date": str(new_date), "description": new_desc
        }, {"id": f"eq.{tx_id}"})
        st.success("Updated!")
        st.rerun()
    if dlt:
        sb_delete("transactions", {"id": f"eq.{tx_id}"})
        st.success("Deleted!")
        st.rerun()

# ─────────────────────────────────────────
# ── FINANCIAL GOALS ──
# ─────────────────────────────────────────
elif menu == "🎯 Goals":
    page_header("Financial Goals", "// set targets. smash them.")

    # ── Add goal form ──
    with st.expander("➕ Add new goal", expanded=False):
        with st.form("add_goal"):
            c1, c2 = st.columns(2)
            g_name    = c1.text_input("Goal name (e.g. Emergency Fund)")
            g_icon    = c2.selectbox("Icon", ["🏠","🚗","✈️","📱","💍","🎓","🏥","💼","🌍","🎯"])
            c3, c4, c5 = st.columns(3)
            g_target  = c3.number_input("Target amount (₹)", min_value=100.0, value=100000.0, step=1000.0)
            g_saved   = c4.number_input("Already saved (₹)", min_value=0.0, value=0.0, step=500.0)
            g_date    = c5.date_input("Target date", value=date(date.today().year+1, 12, 31))
            g_sub     = st.form_submit_button("Save goal →", use_container_width=True)
        if g_sub:
            if not g_name:
                st.warning("Enter a goal name.")
            else:
                sb_insert("goals", {
                    "user_id": st.session_state.user_id, "name": g_name,
                    "icon": g_icon, "target": g_target, "saved": g_saved,
                    "deadline": str(g_date)
                })
                st.success(f"Goal '{g_name}' created!")
                st.rerun()

    # ── Load goals ──
    goals = sb_select("goals", {"user_id": f"eq.{st.session_state.user_id}"}, order="deadline.asc")

    if not goals:
        st.info("No goals yet. Add your first financial goal above.")
        st.stop()

    st.markdown(f'<div class="fv-page-sub">// {len(goals)} active goal(s)</div>', unsafe_allow_html=True)

    for g in goals:
        gid, gname, gicon, gtarget, gsaved, gdeadline = g["id"], g["name"], g.get("icon","target"), float(g["target"]), float(g.get("saved",0)), g["deadline"]
        pct    = min(100, (gsaved / gtarget * 100) if gtarget > 0 else 0)
        remain = gtarget - gsaved
        days_left = (datetime.strptime(gdeadline, "%Y-%m-%d").date() - date.today()).days
        fill   = GREEN if pct >= 80 else (GOLD if pct >= 40 else RED)
        done   = pct >= 100

        st.markdown(f"""<div class="glass-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div>
                    <span style="font-size:1.4rem;">{gicon}</span>
                    <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;
                        color:#e8e8e8;margin-left:8px;">{gname}</span>
                    {'<span class="kpi-pill kpi-pill-green" style="margin-left:8px;">✓ DONE</span>' if done else ''}
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'DM Mono',monospace;font-size:1.1rem;font-weight:500;color:{fill};">
                        ₹{gsaved:,.0f} <span style="color:#444;font-size:0.8rem;">/ ₹{gtarget:,.0f}</span></div>
                    <div style="font-size:0.72rem;color:#555;font-family:'DM Mono',monospace;">
                        {'🎉 achieved!' if done else f'{days_left}d left · ₹{remain:,.0f} to go'}</div>
                </div>
            </div>
            <div class="budget-bar-bg">
                <div class="budget-bar-fill" style="width:{pct:.1f}%;background:{fill};
                    box-shadow:0 0 8px {fill}55;"></div>
            </div>
            <div style="font-size:0.72rem;color:#444;font-family:'DM Mono',monospace;text-align:right;">
                {pct:.1f}% complete · deadline {gdeadline}</div>
        </div>""", unsafe_allow_html=True)

        col_add, col_del = st.columns([3, 1])
        add_amt = col_add.number_input(f"Add savings to '{gname}'", min_value=0.0,
                                        step=500.0, key=f"gadd_{gid}")
        with col_del:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save", key=f"gsave_{gid}"):
                sb_update("goals", {"saved": gsaved + add_amt}, {"id": f"eq.{gid}"})
                st.success(f"+₹{add_amt:,.0f} added!")
                st.rerun()

        if st.button("🗑️ Delete goal", key=f"gdel_{gid}"):
            sb_delete("goals", {"id": f"eq.{gid}"})
            st.rerun()

    # Summary chart
    if len(goals) > 1:
        st.divider()
        st.markdown('<div class="fv-section-title">goals overview</div>', unsafe_allow_html=True)
        gnames  = [g["name"] for g in goals]
        gtargs  = [g["target"] for g in goals]
        gsaveds = [g["saved"] for g in goals]
        fig_g = go.Figure()
        fig_g.add_trace(go.Bar(name="Saved", x=gnames, y=gsaveds,
                               marker_color=GREEN, marker_line_width=0,
                               hovertemplate="<b>%{x}</b><br>Saved: ₹%{y:,.0f}<extra></extra>"))
        fig_g.add_trace(go.Bar(name="Remaining", x=gnames,
                               y=[max(0, t-s) for t,s in zip(gtargs, gsaveds)],
                               marker_color="rgba(255,255,255,0.06)", marker_line_width=0,
                               hovertemplate="<b>%{x}</b><br>Remaining: ₹%{y:,.0f}<extra></extra>"))
        fig_g.update_layout(**plotly_base(280), barmode="stack", bargap=0.3)
        st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────
# ── GAMIFICATION ──
# ─────────────────────────────────────────
elif menu == "🏆 Achievements":
    page_header("Achievements", "// grind. earn. flex.")

    df    = load_transactions(st.session_state.user_id)
    score, _ = compute_health_score(df)

    # Compute stats
    total_tx     = len(df)
    total_inc    = df[df["Type"]=="Income"]["Amount_INR"].sum() if not df.empty else 0
    total_exp    = df[df["Type"]=="Expense"]["Amount_INR"].sum() if not df.empty else 0
    savings      = total_inc - total_exp
    months_active= df["Date"].dt.to_period("M").nunique() if not df.empty else 0
    categories   = df["Category"].nunique() if not df.empty else 0
    recurring_ct = df[df["Recurring"]==1]["Category"].nunique() if not df.empty else 0

    # XP system
    xp = (total_tx * 10) + (months_active * 50) + (score * 5) + (int(savings > 0) * 100)
    level = max(1, xp // 200 + 1)
    xp_in_level  = xp % 200
    xp_next      = 200
    rank = "BRONZE" if level < 5 else "SILVER" if level < 10 else "GOLD" if level < 20 else "DIAMOND"
    rank_color = {"BRONZE":"#cd7f32","SILVER":"#c0c0c0","GOLD":GOLD,"DIAMOND":CYAN}[rank]

    # Level card
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown(f"""<div class="glass-card" style="text-align:center;padding:1.5rem;">
            <div style="font-size:2.5rem;">{"🥉" if rank=="BRONZE" else "🥈" if rank=="SILVER" else "🥇" if rank=="GOLD" else "💎"}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:{rank_color};
                letter-spacing:0.12em;margin:4px 0;">{rank}</div>
            <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                color:{rank_color};">LVL {level}</div>
            <div style="font-size:0.72rem;color:#555;font-family:'DM Mono',monospace;">{xp} XP total</div>
            <div class="budget-bar-bg" style="margin-top:10px;">
                <div class="budget-bar-fill" style="width:{xp_in_level/xp_next*100:.0f}%;
                    background:{rank_color};box-shadow:0 0 8px {rank_color}66;"></div>
            </div>
            <div style="font-size:0.68rem;color:#444;font-family:'DM Mono',monospace;">
                {xp_in_level}/{xp_next} XP to next level</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="fv-section-title">XP breakdown</div>', unsafe_allow_html=True)
        xp_items = [
            ("Transactions logged", total_tx, total_tx*10, "📝"),
            ("Months active", months_active, months_active*50, "📅"),
            ("Health score bonus", score, score*5, "⭐"),
            ("Positive savings bonus", 1 if savings>0 else 0, 100 if savings>0 else 0, "💰"),
        ]
        for label, val, pts, icon in xp_items:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                align-items:center;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="font-size:0.85rem;color:#aaa;">{icon} {label}: <b style="color:#e0e0e0;">{val}</b></span>
                <span class="kpi-pill kpi-pill-green">+{pts} XP</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="fv-section-title">🎖️ badges</div>', unsafe_allow_html=True)

    badges = [
        ("🌱", "First Steps",       "Log your first transaction",    total_tx >= 1),
        ("📊", "Data Nerd",         "Log 10+ transactions",          total_tx >= 10),
        ("🔥", "On Fire",           "Log 50+ transactions",          total_tx >= 50),
        ("💰", "Saver",             "Have positive savings",         savings > 0),
        ("🏦", "Big Saver",         "Save over ₹50,000",             savings > 50000),
        ("🗓️", "Consistent",        "Active for 3+ months",          months_active >= 3),
        ("📆", "Veteran",           "Active for 6+ months",          months_active >= 6),
        ("🎯", "Diversified",       "Use 5+ categories",             categories >= 5),
        ("🔄", "Automator",         "Set up recurring transactions", recurring_ct >= 1),
        ("⭐", "Financially Fit",   "Health score 70+",              score >= 70),
        ("🏆", "Elite",             "Health score 90+",              score >= 90),
        ("💎", "Diamond Hands",     "Reach Level 10",                level >= 10),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc, earned) in enumerate(badges):
        opacity = "1" if earned else "0.25"
        border  = f"rgba(0,229,160,0.3)" if earned else "rgba(255,255,255,0.05)"
        glow    = f"box-shadow:0 0 14px rgba(0,229,160,0.2);" if earned else ""
        cols[i%3].markdown(f"""<div style="background:rgba(255,255,255,0.02);
            border:1px solid {border};border-radius:14px;padding:0.9rem 1rem;
            margin-bottom:0.6rem;opacity:{opacity};{glow}">
            <div style="font-size:1.5rem;">{icon}</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.85rem;
                color:#e0e0e0;margin:4px 0 2px;">{name}</div>
            <div style="font-size:0.7rem;color:#555;font-family:'DM Mono',monospace;">{desc}</div>
            {'<div class="kpi-pill kpi-pill-green" style="margin-top:6px;">EARNED</div>' if earned else
             '<div style="font-size:0.68rem;color:#333;margin-top:4px;">locked</div>'}
        </div>""", unsafe_allow_html=True)

    # Streaks
    st.divider()
    st.markdown('<div class="fv-section-title">🔥 streaks</div>', unsafe_allow_html=True)
    if not df.empty:
        df_s = df.copy()
        df_s["Month"] = df_s["Date"].dt.to_period("M")
        month_counts  = df_s.groupby("Month").size()
        streak = 0
        cur    = pd.Period(date.today(), freq="M")
        while cur in month_counts.index:
            streak += 1; cur -= 1
        c1,c2,c3 = st.columns(3)
        c1.metric("🔥 Current streak", f"{streak} month{'s' if streak!=1 else ''}")
        c2.metric("📝 Total transactions", total_tx)
        c3.metric("📅 Months active", months_active)
    else:
        st.info("Start logging transactions to build your streak!")


# ─────────────────────────────────────────
# ── BILL REMINDERS ──
# ─────────────────────────────────────────
elif menu == "📅 Bills":
    page_header("Bill Reminders", "// never miss a due date")

    with st.expander("➕ Add bill reminder", expanded=False):
        with st.form("add_bill"):
            c1, c2 = st.columns(2)
            b_name   = c1.text_input("Bill name (e.g. Electricity)")
            b_icon   = c2.selectbox("Icon", ["💡","🌐","📱","🏠","🚗","💳","🎓","💧","🔥","📺"])
            c3, c4, c5 = st.columns(3)
            b_amt    = c3.number_input("Amount (₹)", min_value=0.0, value=1000.0, step=100.0)
            b_due    = c4.number_input("Due day of month", min_value=1, max_value=31, value=1)
            b_freq   = c5.selectbox("Frequency", ["Monthly","Quarterly","Yearly"])
            b_sub    = st.form_submit_button("Save reminder →", use_container_width=True)
        if b_sub:
            if not b_name:
                st.warning("Enter a bill name.")
            else:
                sb_insert("bills", {
                    "user_id": st.session_state.user_id, "name": b_name,
                    "icon": b_icon, "amount": b_amt,
                    "due_day": int(b_due), "frequency": b_freq
                })
                st.success(f"Bill '{b_name}' reminder saved!")
                st.rerun()

    bills = sb_select("bills", {"user_id": f"eq.{st.session_state.user_id}"}, order="due_day.asc")

    if not bills:
        st.info("No bill reminders yet. Add your recurring bills above.")
        st.stop()

    today       = date.today()
    this_month  = today.month
    this_year   = today.year

    overdue, due_soon, upcoming = [], [], []
    for b in bills:
        try:
            due_date = date(this_year, this_month, min(b["due_day"], 28))
        except:
            due_date = date(this_year, this_month, 28)
        days_diff = (due_date - today).days
        if days_diff < 0:
            overdue.append((b, due_date, days_diff))
        elif days_diff <= 5:
            due_soon.append((b, due_date, days_diff))
        else:
            upcoming.append((b, due_date, days_diff))

    # Summary KPIs
    total_monthly = sum(b["amount"] for b in bills if b["frequency"]=="Monthly")
    c1,c2,c3 = st.columns(3)
    c1.metric("📋 Total bills", len(bills))
    c2.metric("🔴 Overdue", len(overdue))
    c3.metric("💸 Monthly total", f"₹{total_monthly:,.0f}")

    def bill_card(b, due_date, days_diff, status):
        color  = RED if status=="overdue" else (GOLD if status=="soon" else GREEN)
        tag    = f'<span class="kpi-pill kpi-pill-red">OVERDUE {abs(days_diff)}d</span>' if status=="overdue" else \
                 f'<span class="kpi-pill kpi-pill-gold">DUE IN {days_diff}d</span>' if status=="soon" else \
                 f'<span class="kpi-pill kpi-pill-green">IN {days_diff}d</span>'
        st.markdown(f"""<div class="glass-card" style="border-color:{color}22;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <span style="font-size:1.6rem;">{b["icon"]}</span>
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-weight:700;
                            color:#e0e0e0;font-size:0.92rem;">{b["name"]}</div>
                        <div style="font-size:0.72rem;color:#555;font-family:'DM Mono',monospace;">
                            {b["frequency"]} · due {due_date.strftime("%d %b")}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'DM Mono',monospace;font-size:1.1rem;
                        color:{color};font-weight:600;">₹{b["amount"]:,.0f}</div>
                    {tag}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Remove", key=f"bdel_{b['id']}]"):
            sb_delete("bills", {"id": f"eq.{b['id']}"})
            st.rerun()

    if overdue:
        st.markdown('<div class="fv-section-title" style="color:#ff6060;">🔴 overdue</div>', unsafe_allow_html=True)
        for b, d, diff in overdue: bill_card(b, d, diff, "overdue")

    if due_soon:
        st.markdown('<div class="fv-section-title" style="color:#c8a800;">⚠️ due soon</div>', unsafe_allow_html=True)
        for b, d, diff in due_soon: bill_card(b, d, diff, "soon")

    if upcoming:
        st.markdown('<div class="fv-section-title">📅 upcoming</div>', unsafe_allow_html=True)
        for b, d, diff in upcoming: bill_card(b, d, diff, "ok")

    # Timeline chart
    if bills:
        st.divider()
        st.markdown('<div class="fv-section-title">📊 bill timeline this month</div>', unsafe_allow_html=True)
        bill_names = [b["name"] for b in bills]
        bill_days  = [min(b["due_day"], 28) for b in bills]
        bill_amts  = [b["amount"] for b in bills]
        colors     = [RED if d < today.day else (GOLD if d <= today.day+5 else GREEN) for d in bill_days]
        fig_b = go.Figure(go.Bar(
            x=bill_days, y=bill_names, orientation="h",
            marker=dict(color=colors, line_width=0),
            text=[f"₹{a:,.0f}" for a in bill_amts],
            textposition="inside", textfont=dict(color="#080808", size=10),
            hovertemplate="<b>%{y}</b><br>Day %{x}<extra></extra>",
        ))
        fig_b.add_vline(x=today.day, line_color=CYAN, line_dash="dot", line_width=1.5,
                        annotation_text="today", annotation_font_color=CYAN,
                        annotation_font_size=10)
        fig_b.update_layout(**plotly_base(max(200, len(bills)*45)),
                            xaxis_title="Day of month", xaxis=dict(range=[0,32]))
        st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────
# ── RECEIPT SCANNER ──
# ─────────────────────────────────────────
elif menu == "📸 Scan Receipt":
    page_header("Receipt Scanner", "// snap. extract. log.")

    st.markdown("""<div class="glass-card">
        <div class="fv-section-title">how it works</div>
        <div style="font-size:0.82rem;color:#666;font-family:'DM Mono',monospace;line-height:1.8;">
        1. Upload a photo or scan of your receipt<br>
        2. We extract text using OCR<br>
        3. Review the detected amounts<br>
        4. Log directly as a transaction
        </div>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload receipt image", type=["png","jpg","jpeg","webp","bmp"])

    if uploaded:
        from PIL import Image
        import re

        img = Image.open(uploaded)
        st.image(img, caption="Uploaded receipt", use_container_width=False, width=350)

        st.markdown('<div class="fv-section-title">extracted text</div>', unsafe_allow_html=True)

        # Try pytesseract, fall back to pattern-based mock if tesseract not installed
        raw_text = ""
        try:
            import pytesseract
            raw_text = pytesseract.image_to_string(img)
        except Exception:
            raw_text = "[Tesseract not installed on this system — install it with: choco install tesseract  (Windows) or  brew install tesseract  (Mac)]"

        st.code(raw_text if raw_text.strip() else "No text detected.", language=None)

        # Extract amounts from text
        amounts = re.findall(r"(?:rs\.?|inr|₹)?\s*(\d{1,6}(?:[.,]\d{2})?)", raw_text, re.IGNORECASE)
        amounts = [float(a.replace(",","")) for a in amounts if float(a.replace(",","")) > 0]

        if amounts:
            st.markdown('<div class="fv-section-title">detected amounts</div>', unsafe_allow_html=True)
            best_amt = max(amounts)  # assume largest = total

            c1, c2 = st.columns(2)
            c1.markdown(f"""<div class="glass-card">
                <div class="kpi-label-sm">likely total</div>
                <div class="kpi-big" style="color:{GREEN};">₹{best_amt:,.2f}</div>
                <div style="font-size:0.72rem;color:#444;font-family:'DM Mono',monospace;margin-top:4px;">
                    all detected: {", ".join([f"₹{a:,.0f}" for a in sorted(set(amounts), reverse=True)[:5]])}</div>
            </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="fv-section-title">log as transaction</div>', unsafe_allow_html=True)
                with st.form("receipt_tx"):
                    r_cat  = st.text_input("Category", value="Shopping")
                    r_amt  = st.number_input("Amount (₹)", value=float(best_amt), min_value=0.01)
                    r_date = st.date_input("Date", value=date.today())
                    r_desc = st.text_area("Note", value="From scanned receipt", height=60)
                    r_sub  = st.form_submit_button("Log expense →", use_container_width=True)
                if r_sub:
                    sb_insert("transactions", {
                        "user_id": st.session_state.user_id, "type": "Expense",
                        "category": r_cat, "amount": r_amt, "date": str(r_date),
                        "description": r_desc, "currency": "INR", "amount_inr": r_amt
                    })
                    st.success(f"✅ Logged ₹{r_amt:,.2f} as {r_cat}!")
        else:
            st.info("No amounts detected in the image. You can still log manually below.")
            with st.form("manual_receipt_tx"):
                r_cat  = st.text_input("Category")
                r_amt  = st.number_input("Amount (₹)", min_value=0.01, value=100.0)
                r_date = st.date_input("Date", value=date.today())
                r_desc = st.text_area("Note", value="Receipt scan")
                r_sub  = st.form_submit_button("Log expense →", use_container_width=True)
            if r_sub and r_cat:
                sb_insert("transactions", {
                    "user_id": st.session_state.user_id, "type": "Expense",
                    "category": r_cat, "amount": r_amt, "date": str(r_date),
                    "description": r_desc, "currency": "INR", "amount_inr": r_amt
                })
                st.success(f"✅ Logged ₹{r_amt:,.2f} as {r_cat}!")

    else:
        st.markdown("""<div style="border:2px dashed rgba(0,229,160,0.15);border-radius:16px;
            padding:3rem;text-align:center;color:#444;">
            <div style="font-size:2.5rem;margin-bottom:0.5rem;">📸</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.8rem;letter-spacing:0.06em;">
            drag & drop or click above to upload</div>
        </div>""", unsafe_allow_html=True)