import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime
import io
import requests as _req

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
# Detect mobile via query params not possible in Streamlit,
# so we default sidebar collapsed — desktop users can expand
import os
st.set_page_config(
    page_title="FinVault · AI Budget Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# GLOBAL THEME — Black + Neon Green/Gold Glassmorphism
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════
   FINVAULT — DARK LIQUID GLASS THEME
   Mobile-first, glossy, premium banking UI
   ═══════════════════════════════════════════ */

/* ── Tokens ── */
:root {
    --bg:          #08090f;
    --surface:     rgba(255,255,255,0.04);
    --surface-2:   rgba(255,255,255,0.07);
    --border:      rgba(255,255,255,0.08);
    --border-hi:   rgba(255,255,255,0.14);
    --blue:        #1a56ff;
    --blue-glow:   rgba(26,86,255,0.35);
    --orange:      #f47920;
    --orange-glow: rgba(244,121,32,0.3);
    --green:       #00c87a;
    --green-glow:  rgba(0,200,122,0.3);
    --red:         #ff4040;
    --red-glow:    rgba(255,64,64,0.3);
    --text:        #e8edf8;
    --text-muted:  #6a7590;
    --text-dim:    #3a4260;
    --glass-shine: rgba(255,255,255,0.06);
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
}
[data-testid="stAppViewContainer"] > .main { background: var(--bg) !important; }
[data-testid="block-container"] { padding-top: 0.5rem !important; padding-bottom: 5rem !important; }
[data-testid="stMainBlockContainer"] {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

/* ══════════════════════════════════════
   SIDEBAR — CLEAN DARK GLASS
   ══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: rgba(8,9,15,0.97) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    min-width: 220px !important;
    max-width: 240px !important;
}
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Radio nav items */
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 7px 12px !important;
    margin: 1px 0 !important;
    transition: background 0.15s !important;
    width: 100% !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    font-family: Inter, sans-serif !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover p,
[data-testid="stSidebar"] [role="radiogroup"] label:hover span {
    color: #ffffff !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] {
    background: rgba(26,86,255,0.12) !important;
    border-left: 2px solid var(--blue) !important;
    border-radius: 0 10px 10px 0 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] p,
[data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Hide bottom nav on desktop */
@media (min-width: 769px) {
    .fv-bottom-nav { display: none !important; }
}

/* Mobile: sidebar hidden by default but toggle always visible */
@media (max-width: 768px) {
    /* Keep sidebar toggle button always visible and styled */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 12px !important;
        left: 12px !important;
        z-index: 9998 !important;
        background: rgba(26,86,255,0.15) !important;
        border: 1px solid rgba(26,86,255,0.3) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        backdrop-filter: blur(10px) !important;
    }
    [data-testid="collapsedControl"] button {
        color: #ffffff !important;
    }
    /* Sidebar slides in as overlay */
    [data-testid="stSidebar"] {
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        height: 100vh !important;
        z-index: 9997 !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.5) !important;
    }
    .fv-bottom-nav { display: flex !important; }
    [data-testid="stMainBlockContainer"] {
        padding-bottom: 90px !important;
        padding-top: 3.5rem !important;
    }
}

/* ── Page transition ── */
[data-testid="stMainBlockContainer"] {
    animation: fadeUp 0.4s cubic-bezier(0.16,1,0.3,1) !important;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════
   LIQUID GLASS MIXIN
   ══════════════════════════ */
.glass {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-top-color: rgba(255,255,255,0.14) !important;
    border-left-color: rgba(255,255,255,0.1) !important;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(255,255,255,0.08),
        inset 0 -1px 0 rgba(0,0,0,0.2) !important;
}

/* ── Inputs — glass style ── */
input, textarea,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border-hi) !important;
    border-top-color: rgba(255,255,255,0.16) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    caret-color: var(--blue) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 0.9rem !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 4px 12px rgba(0,0,0,0.3) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus, textarea:focus {
    border-color: rgba(26,86,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(26,86,255,0.15),
                inset 0 1px 0 rgba(255,255,255,0.08) !important;
    outline: none !important;
}
input:-webkit-autofill, input:-webkit-autofill:hover,
input:-webkit-autofill:focus, input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 9999px #0f1120 inset !important;
    -webkit-text-fill-color: var(--text) !important;
}
input::placeholder, textarea::placeholder {
    color: var(--text-dim) !important;
    -webkit-text-fill-color: var(--text-dim) !important;
}
[data-baseweb="input"], [data-baseweb="base-input"],
[data-testid="stTextInput"] > div, [data-testid="stNumberInput"] > div {
    background: transparent !important;
    border-radius: 12px !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
[data-baseweb="select"] * { color: var(--text) !important; }
label, [data-testid="stWidgetLabel"] p {
    color: var(--text-muted) !important;
    -webkit-text-fill-color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Buttons — glossy pill ── */
.stButton > button {
    background: linear-gradient(135deg,
        rgba(26,86,255,0.9) 0%,
        rgba(10,50,200,0.95) 100%) !important;
    backdrop-filter: blur(10px) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.8rem !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    box-shadow:
        0 4px 20px rgba(26,86,255,0.35),
        inset 0 1px 0 rgba(255,255,255,0.2),
        inset 0 -1px 0 rgba(0,0,0,0.15) !important;
    transition: all 0.2s cubic-bezier(0.16,1,0.3,1) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(26,86,255,0.5),
                inset 0 1px 0 rgba(255,255,255,0.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
.stDownloadButton > button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--border) !important;
    border-top-color: rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3),
                inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 1.4rem !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    -webkit-text-fill-color: var(--text-muted) !important;
    font-size: 0.74rem !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
.dvn-scroller { background: transparent !important; }

/* ── Progress bars ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--blue), var(--orange)) !important;
    border-radius: 999px !important;
    box-shadow: 0 0 8px var(--blue-glow) !important;
}
[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 999px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
}
[data-testid="stExpander"] summary { color: var(--text) !important; font-weight: 500 !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(26,86,255,0.08) !important;
    border: 1px solid rgba(26,86,255,0.2) !important;
    border-left: 3px solid var(--blue) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
}
[data-testid="stAlert"] p { color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; }

/* ── Form ── */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-top-color: rgba(255,255,255,0.12) !important;
    border-radius: 20px !important;
    padding: 1.4rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.06) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

/* ═══════════════════════════════════════
   FINVAULT COMPONENTS
   ═══════════════════════════════════════ */

/* ── Top app bar (mobile) ── */
.fv-appbar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(8,9,15,0.85);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid var(--border);
    padding: 12px 16px;
    display: flex; align-items: center; justify-content: space-between;
    margin: -0.5rem -1rem 1rem;
    box-shadow: 0 1px 0 rgba(255,255,255,0.04);
}
.fv-appbar-logo {
    font-family: 'Inter', sans-serif; font-weight: 700;
    font-size: 1.1rem; color: #ffffff; letter-spacing: -0.01em;
    display: flex; align-items: center; gap: 8px;
}
.fv-appbar-logo-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--blue);
    box-shadow: 0 0 8px var(--blue-glow);
    animation: pulse 2s ease infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.7; transform: scale(0.85); }
}
.fv-appbar-right {
    font-family: 'DM Mono', monospace; font-size: 0.7rem;
    color: var(--text-muted); letter-spacing: 0.04em;
}

/* ── Ticker ── */
.fv-ticker-wrap {
    overflow: hidden; width: 100%;
    background: rgba(26,86,255,0.08);
    border: 1px solid rgba(26,86,255,0.15);
    border-radius: 10px; padding: 7px 0;
    margin-bottom: 1rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
}
.fv-ticker {
    display: inline-block; white-space: nowrap;
    font-family: 'DM Mono', monospace; font-size: 0.7rem;
    color: rgba(100,160,255,0.9); letter-spacing: 0.06em;
    animation: tickerScroll 36s linear infinite;
}
@keyframes tickerScroll {
    from { transform: translateX(100vw); }
    to   { transform: translateX(-100%); }
}

/* ── Hero card — liquid glass ── */
.fv-hero {
    background: linear-gradient(135deg,
        rgba(26,86,255,0.12) 0%,
        rgba(10,20,60,0.6) 40%,
        rgba(244,121,32,0.06) 100%);
    backdrop-filter: blur(24px) saturate(200%);
    -webkit-backdrop-filter: blur(24px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.1);
    border-top-color: rgba(255,255,255,0.18);
    border-radius: 22px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.5),
        0 0 0 1px rgba(26,86,255,0.1),
        inset 0 1px 0 rgba(255,255,255,0.12),
        inset 0 -1px 0 rgba(0,0,0,0.2);
}
.fv-hero::before {
    content: "";
    position: absolute; top: -80px; right: -60px;
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(26,86,255,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.fv-hero::after {
    content: "";
    position: absolute; bottom: -50px; left: 40%;
    width: 160px; height: 160px; border-radius: 50%;
    background: radial-gradient(circle, rgba(244,121,32,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.fv-hero-greeting {
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size: clamp(1.1rem, 3.5vw, 1.5rem);
    color: #ffffff; letter-spacing: -0.01em; margin-bottom: 3px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
.fv-hero-sub {
    font-family: 'Inter', sans-serif; font-size: 0.76rem;
    color: rgba(255,255,255,0.5); margin-top: 2px;
}
.fv-hero-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem; margin-top: 1.1rem;
}
.fv-hero-stat {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 0.6rem 0.8rem;
    backdrop-filter: blur(8px);
}
.fv-hero-stat-val {
    font-family: 'DM Mono', monospace; font-size: 0.95rem;
    font-weight: 500; color: #ffffff;
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
}
.fv-hero-stat-lbl {
    font-size: 0.58rem; color: rgba(255,255,255,0.45);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-top: 1px;
}

/* ── KPI grid ── */
.fv-kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px; margin-bottom: 1rem;
}
.fv-kpi-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.08);
    border-top-color: rgba(255,255,255,0.13);
    border-radius: 18px;
    padding: 0.9rem 1rem;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3),
                inset 0 1px 0 rgba(255,255,255,0.07);
    transition: transform 0.2s, box-shadow 0.2s;
}
.fv-kpi-card:active { transform: scale(0.97); }
.fv-kpi-card::before {
    content: ""; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    border-radius: 18px 18px 0 0;
}
.fv-kpi-income::before  { background: linear-gradient(90deg, var(--green), transparent); }
.fv-kpi-expense::before { background: linear-gradient(90deg, var(--red), transparent); }
.fv-kpi-savings::before { background: linear-gradient(90deg, var(--orange), transparent); }
.fv-kpi-score::before   { background: linear-gradient(90deg, var(--blue), transparent); }
.fv-kpi-card::after {
    content: ""; position: absolute;
    top: -30px; right: -20px;
    width: 90px; height: 90px; border-radius: 50%; opacity: 0.06;
}
.fv-kpi-income::after  { background: var(--green); }
.fv-kpi-expense::after { background: var(--red); }
.fv-kpi-savings::after { background: var(--orange); }
.fv-kpi-score::after   { background: var(--blue); }
.fv-kpi-tag {
    font-family: 'DM Mono', monospace; font-size: 0.6rem;
    letter-spacing: 0.1em; font-weight: 600;
    padding: 2px 7px; border-radius: 5px;
    margin-bottom: 5px; display: inline-block; text-transform: uppercase;
}
.fv-kpi-val {
    font-family: 'DM Mono', monospace;
    font-size: clamp(1rem, 3vw, 1.4rem);
    font-weight: 500; letter-spacing: -0.02em;
    line-height: 1.1; margin: 2px 0;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.fv-kpi-label {
    font-size: 0.65rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.07em;
    -webkit-text-fill-color: var(--text-muted);
}
.fv-sparkline { margin-top: 6px; opacity: 0.9; }

/* ── Chart card — liquid glass ── */
.fv-chart-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.07);
    border-top-color: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 1rem 1rem 0.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.06);
}

/* ── iOS floating nav ── */
.fv-ios-nav {
    display: none;
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 99999;
    width: auto;
    background: rgba(18, 20, 32, 0.88);
    backdrop-filter: blur(30px) saturate(200%);
    -webkit-backdrop-filter: blur(30px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.12);
    border-top-color: rgba(255,255,255,0.2);
    border-radius: 28px;
    padding: 10px 12px;
    gap: 4px;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.7),
        0 0 0 1px rgba(255,255,255,0.05),
        inset 0 1px 0 rgba(255,255,255,0.1);
}
.fv-ios-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    padding: 8px 14px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    min-width: 52px;
    -webkit-tap-highlight-color: transparent;
}
.fv-ios-nav-item:active {
    transform: scale(0.88);
}
.fv-ios-nav-item.active {
    background: rgba(26,86,255,0.2);
    box-shadow: 0 0 16px rgba(26,86,255,0.25),
                inset 0 1px 0 rgba(255,255,255,0.1);
}
.fv-ios-nav-icon {
    font-size: 1.3rem;
    line-height: 1;
    transition: transform 0.2s;
}
.fv-ios-nav-item.active .fv-ios-nav-icon {
    transform: scale(1.15);
}
.fv-ios-nav-label {
    font-family: Inter, sans-serif;
    font-size: 0.55rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    color: rgba(255,255,255,0.45);
    -webkit-text-fill-color: rgba(255,255,255,0.45);
    transition: color 0.2s;
}
.fv-ios-nav-item.active .fv-ios-nav-label {
    color: #6496ff;
    -webkit-text-fill-color: #6496ff;
}
/* Dot indicator for active */
.fv-ios-nav-dot {
    width: 4px; height: 4px;
    border-radius: 50%;
    background: #1a56ff;
    margin: 0 auto;
    opacity: 0;
    transition: opacity 0.2s;
}
.fv-ios-nav-item.active .fv-ios-nav-dot {
    opacity: 1;
}

/* Show on mobile only */
@media (max-width: 768px) {
    .fv-ios-nav { display: flex !important; }
    [data-testid="block-container"],
    [data-testid="stMainBlockContainer"] {
        padding-bottom: 110px !important;
    }
    /* Hide the Streamlit nav trigger buttons visually */
    div[data-testid="stHorizontalBlock"]:has(button) > div[data-testid="column"] > div > div > div > button {
        opacity: 0 !important;
        height: 1px !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }
}

/* ── Page title ── */
.fv-page-title {
    font-family: 'Inter', sans-serif; font-size: 1.5rem;
    font-weight: 700; letter-spacing: -0.02em; color: #ffffff;
    margin-bottom: 0.1rem;
}
.fv-page-sub {
    font-size: 0.76rem; color: var(--text-muted);
    margin-bottom: 1.2rem; font-family: 'Inter', sans-serif;
    -webkit-text-fill-color: var(--text-muted);
}

/* ── Section tags ── */
.section-tag {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.62rem; font-weight: 600; padding: 2px 9px;
    border-radius: 6px; background: rgba(26,86,255,0.1);
    color: rgba(100,160,255,0.9);
    border: 1px solid rgba(26,86,255,0.2);
    letter-spacing: 0.1em; margin-bottom: 3px; text-transform: uppercase;
}
.fv-section-title {
    font-family: 'Inter', sans-serif; font-size: 0.95rem;
    font-weight: 600; color: var(--text); margin-bottom: 0.7rem;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.08);
    border-top-color: rgba(255,255,255,0.13);
    border-radius: 18px; padding: 1.2rem 1.3rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3),
                inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative; overflow: hidden;
}
.glass-card::after { display: none !important; }

/* ── Pills ── */
.kpi-pill {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.62rem; font-weight: 500; padding: 2px 9px;
    border-radius: 6px; letter-spacing: 0.06em; margin-bottom: 5px;
    text-transform: uppercase;
}
.kpi-pill-green { background: rgba(0,200,122,0.1);  color: #00c87a; border: 1px solid rgba(0,200,122,0.2); }
.kpi-pill-gold  { background: rgba(244,121,32,0.1); color: #f47920; border: 1px solid rgba(244,121,32,0.2); }
.kpi-pill-red   { background: rgba(255,64,64,0.1);  color: #ff4040; border: 1px solid rgba(255,64,64,0.2); }
.kpi-pill-cyan  { background: rgba(26,86,255,0.1);  color: #6496ff; border: 1px solid rgba(26,86,255,0.2); }

/* ── kpi-big / kpi-label-sm ── */
.kpi-big {
    font-family: 'DM Mono', monospace; font-size: 1.7rem;
    font-weight: 500; letter-spacing: -0.02em;
    line-height: 1; margin: 4px 0 2px; color: #ffffff;
}
.kpi-label-sm {
    font-size: 0.68rem; color: var(--text-muted);
    letter-spacing: 0.07em; text-transform: uppercase;
    -webkit-text-fill-color: var(--text-muted);
}

/* ── Sidebar logo / user badge (used in non-mobile) ── */
.sidebar-logo {
    font-family: 'Inter', sans-serif; font-size: 1.2rem;
    font-weight: 700; color: #ffffff; letter-spacing: -0.01em;
    padding: 0.5rem 0 0.1rem;
}
.sidebar-tagline {
    font-size: 0.64rem; color: var(--text-dim);
    letter-spacing: 0.08em; margin-bottom: 1rem;
}
.user-badge {
    background: rgba(26,86,255,0.12);
    border: 1px solid rgba(26,86,255,0.2);
    border-radius: 10px; padding: 8px 12px;
    font-family: 'DM Mono', monospace; font-size: 0.76rem;
    color: #6496ff; margin-bottom: 0.8rem;
    -webkit-text-fill-color: #6496ff;
}

/* ── Budget bars ── */
.budget-bar-bg {
    background: rgba(255,255,255,0.06); border-radius: 999px;
    height: 7px; margin: 4px 0 14px; overflow: hidden;
}
.budget-bar-fill { height: 7px; border-radius: 999px; }

/* ── Invest cards ── */
.invest-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.07);
    border-top-color: rgba(255,255,255,0.11);
    border-radius: 14px; padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25),
                inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
}
.invest-card:active { transform: scale(0.98); }
.invest-name { font-weight: 600; font-size: 0.88rem; color: var(--text); margin-bottom: 2px; }
.invest-desc { font-size: 0.74rem; color: var(--text-muted); }

/* ── Home features ── */
.home-feature {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 0.8rem 1rem;
    margin-bottom: 0.4rem; font-size: 0.84rem;
    color: var(--text); display: flex; gap: 10px; align-items: center;
    -webkit-text-fill-color: var(--text);
}
.home-feature span { color: var(--blue); }

/* ═══════════════════════════════════════
   MOBILE FIRST — ALL SCREENS
   ═══════════════════════════════════════ */

/* Desktop: wider padding */
@media (min-width: 769px) {
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(8,10,20,0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: transparent !important; border-radius: 10px !important;
        padding: 7px 14px !important; margin: 1px 0 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label p,
    [data-testid="stSidebar"] [role="radiogroup"] label span {
        color: var(--text-muted) !important; font-size: 0.83rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover p,
    [data-testid="stSidebar"] [role="radiogroup"] label:hover span { color: #ffffff !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none !important; }
    [data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] {
        background: rgba(26,86,255,0.12) !important;
        border-left: 2px solid var(--blue) !important;
        border-radius: 0 10px 10px 0 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] p,
    [data-testid="stSidebar"] [role="radiogroup"] [aria-checked="true"] span {
        color: #ffffff !important; font-weight: 600 !important;
    }
    .fv-bottom-nav { display: none !important; }
    .fv-appbar { display: none !important; }
    .fv-kpi-grid { grid-template-columns: repeat(4, 1fr) !important; gap: 12px !important; }
    .fv-hero-stats { grid-template-columns: repeat(6, 1fr) !important; }
    [data-testid="block-container"] { padding-bottom: 1rem !important; }
    [data-testid="stMainBlockContainer"] {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
}

/* Mobile only */
@media (max-width: 768px) {
    .fv-kpi-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 8px !important; }
    .fv-hero-stats { grid-template-columns: repeat(2, 1fr) !important; gap: 0.6rem !important; }
    .fv-page-title { font-size: 1.25rem !important; }
    .fv-kpi-val { font-size: 1rem !important; }
    .fv-hero-greeting { font-size: 1.1rem !important; }
    .fv-chart-card { padding: 0.8rem 0.8rem 0.4rem !important; border-radius: 16px !important; }
    .fv-hero { border-radius: 18px !important; padding: 1.1rem 1.1rem !important; }
    .fv-bottom-nav { display: flex !important; }
}
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
BG       = "#08090f"
PLOT_BG  = "#0d0f1a"
GRID     = "rgba(255,255,255,0.04)"
FONT_C   = "#6a7590"
GREEN    = "#00c87a"
GOLD     = "#f47920"
RED      = "#ff5050"
CYAN     = "#00dcff"
PURPLE   = "#8b8fff"
PALETTE  = ["#1a56ff","#00c87a","#f47920","#ff4040","#8b8fff","#00d4ff","#ffb020","#ff6090"]

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

# Add payment_mode column if not exists (runs silently)
try:
    _req.post(
        f"{_SB_URL}/rest/v1/rpc/exec_sql",
        headers=_HEADERS,
        json={"query": "ALTER TABLE transactions ADD COLUMN IF NOT EXISTS payment_mode TEXT DEFAULT 'Cash'"}
    )
except Exception:
    pass

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
for k, v in [("logged_in", False), ("user_id", None), ("username", "")]:
    if k not in st.session_state: st.session_state[k] = v

# Inject JS to detect mobile and collapse sidebar
st.markdown("""
<script>
(function() {
    function isMobile() { return window.innerWidth <= 768; }
    function collapseSidebar() {
        if (isMobile()) {
            var btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
            if (btn) {
                var expanded = window.parent.document.querySelector('[data-testid="stSidebar"][aria-expanded="true"]');
                if (expanded) btn.click();
            }
        }
    }
    if (document.readyState === 'complete') collapseSidebar();
    else window.addEventListener('load', collapseSidebar);
})();
</script>
""", unsafe_allow_html=True)

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
                                  "Description","Recurring","Frequency","Currency","Amount_INR","Payment_Mode"])

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
# NAVIGATION
# ─────────────────────────────────────────
nav_pages = [
    "📊 Dashboard", "📅 Advanced Analytics", "➕ Add Transaction", "🔄 Recurring",
    "🔎 Search & Filter", "💰 Budget Planner", "⭐ Health Score",
    "📈 Investment Advisor", "🏦 Loan & EMI",
    "🎯 Goals", "🏆 Achievements", "📅 Bills", "📸 Scan Receipt",
    "📄 Export Reports", "✏️ Edit / Delete",
]

# Session state for current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 Dashboard"

if st.session_state.logged_in:
    # ── Desktop sidebar ──
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">FinVault</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">// AI BUDGET PLANNER</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-badge">◉  {st.session_state.username}</div>', unsafe_allow_html=True)
        st.markdown("---")
        selected = st.radio("", nav_pages,
                            index=nav_pages.index(st.session_state.current_page)
                            if st.session_state.current_page in nav_pages else 0,
                            label_visibility="collapsed")
        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()
        st.markdown("<br>" * 3, unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = ""
            st.session_state.current_page = "📊 Dashboard"
            st.rerun()

    menu = st.session_state.current_page

else:
    menu = "🏠 Home"

# ─────────────────────────────────────────
# ── AUTH GATE (mobile + desktop)
# ─────────────────────────────────────────
# ── Dialog modals ──
@st.dialog("Login")
def login_dialog():
    email    = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="your password")
    if st.button("Login", use_container_width=True, type="primary"):
        res = sb_select("users", {"email": f"eq.{email}", "password": f"eq.{password}"})
        user = res[0] if res else None
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id   = user["user_id"]
            st.session_state.username  = user["username"]
            st.rerun()
        else:
            st.error("Invalid credentials.")

@st.dialog("Create Account")
def signup_dialog():
    username = st.text_input("Username", placeholder="e.g. Soham")
    email    = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="min 4 characters")
    if st.button("Create account", use_container_width=True, type="primary"):
        if not username or not email or not password:
            st.warning("Fill in all fields.")
        else:
            try:
                existing = sb_select("users", {"email": f"eq.{email}", "select": "user_id"})
                if existing:
                    st.error("Email already registered.")
                else:
                    sb_insert("users", {"username": username, "email": email, "password": password})
                    new_user = sb_select("users", {"email": f"eq.{email}", "password": f"eq.{password}"})
                    if new_user:
                        st.session_state.logged_in = True
                        st.session_state.user_id   = new_user[0]["user_id"]
                        st.session_state.username  = new_user[0]["username"]
                        st.rerun()
                    else:
                        st.success("Account created! Please login.")
            except Exception as e:
                st.error(f"Error: {e}")

if not st.session_state.logged_in and menu in ["🏠 Home", "🔐 Login", "📝 Signup"]:

    # Mobile top bar
    st.markdown('''<div class="fv-appbar" style="display:flex !important;">
        <div class="fv-appbar-logo">
            <div class="fv-appbar-logo-dot"></div>
            FinVault
        </div>
        <div class="fv-appbar-right">AI Budget Planner</div>
    </div>''', unsafe_allow_html=True)

    # Hero splash
    st.markdown('''<div style="text-align:center;padding:3rem 1rem 2rem;">
        <div style="font-family:'Inter',sans-serif;font-size:2.2rem;font-weight:700;
            color:#ffffff;letter-spacing:-0.03em;line-height:1.2;margin-bottom:10px;">
            Your money,<br>under control.
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.85rem;
            color:rgba(255,255,255,0.4);margin-bottom:2.5rem;">
            AI-powered budget planner & investment advisor
        </div>
    </div>''', unsafe_allow_html=True)

    # CTA buttons — open dialogs
    col_l, col_r = st.columns(2)
    if col_l.button("Login", use_container_width=True, type="primary"):
        login_dialog()
    if col_r.button("Sign up", use_container_width=True):
        signup_dialog()

    # Features grid
    st.markdown("<br>", unsafe_allow_html=True)
    features = [
        ("Dashboard", "Animated charts & KPIs"),
        ("Budget Planner", "Track vs budget alerts"),
        ("Health Score", "AI financial score 0-100"),
        ("Investment Advisor", "Personalised SIP planner"),
        ("Goals Tracker", "Set & track financial goals"),
        ("Bill Reminders", "Never miss a due date"),
    ]
    col1, col2 = st.columns(2)
    for i, (title, desc) in enumerate(features):
        col = col1 if i % 2 == 0 else col2
        col.markdown(f'''<div style="background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.07);border-radius:14px;
            padding:0.8rem 1rem;margin-bottom:0.5rem;">
            <div style="font-size:0.84rem;font-weight:600;color:#e8edf8;">{title}</div>
            <div style="font-size:0.72rem;color:#6a7590;margin-top:2px;">{desc}</div>
        </div>''', unsafe_allow_html=True)

elif not st.session_state.logged_in:
    st.warning("Please login to continue.")

# ─────────────────────────────────────────
# ── DASHBOARD ──
# ─────────────────────────────────────────
elif menu == "📊 Dashboard":
    df = load_transactions(st.session_state.user_id)
    _greet = f"Welcome back, {st.session_state.username}"
    _greet_sub = f"Here is your financial overview for {datetime.today().strftime('%d %B %Y')}."

    if df.empty:
        st.info("No transactions yet — add your first one.")
        st.stop()

    total_inc  = df[df["Type"]=="Income"]["Amount_INR"].sum()
    total_exp  = df[df["Type"]=="Expense"]["Amount_INR"].sum()
    savings    = total_inc - total_exp
    score, _   = compute_health_score(df)
    score_color = GREEN if score >= 70 else (GOLD if score >= 40 else RED)

    # ── Mobile app bar ──
    st.markdown(f'''<div class="fv-appbar">
        <div class="fv-appbar-logo">
            <div class="fv-appbar-logo-dot"></div>
            FinVault
        </div>
        <div class="fv-appbar-right">{datetime.today().strftime("%d %b %Y")}</div>
    </div>''', unsafe_allow_html=True)

    # ── Ticker bar ──
    _ticker_items = [
        f"INCOME   ₹{total_inc:,.0f}",
        f"EXPENSES   ₹{total_exp:,.0f}",
        f"SAVINGS   ₹{savings:,.0f}",
        f"HEALTH SCORE   {score}/100",
        f"TRANSACTIONS   {len(df)}",
        f"DATE   {datetime.today().strftime('%d %b %Y')}",
        f"CATEGORIES   {df['Category'].nunique()}",
        f"SAVINGS RATE   {(savings/total_inc*100) if total_inc > 0 else 0:.1f}%",
    ]
    _ticker_str = "     ●     ".join(_ticker_items) + "     ●     " + "     ●     ".join(_ticker_items)
    st.markdown(f'''<div class="fv-ticker-wrap">
        <span class="fv-ticker">{_ticker_str}</span>
    </div>''', unsafe_allow_html=True)

    # ── Hero greeting card ──
    _savings_pct = (savings/total_inc*100) if total_inc > 0 else 0
    _months = df["Date"].dt.to_period("M").nunique()
    st.markdown(f'''<div class="fv-hero">
        <div class="fv-hero-greeting">{_greet}</div>
        <div class="fv-hero-sub">{datetime.today().strftime("%A, %d %B %Y")} &nbsp;·&nbsp; {_greet_sub}</div>
        <div class="fv-hero-stats">
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">₹{total_inc:,.0f}</span>
                <span class="fv-hero-stat-lbl">Total Income</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">₹{total_exp:,.0f}</span>
                <span class="fv-hero-stat-lbl">Total Spent</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">₹{savings:,.0f}</span>
                <span class="fv-hero-stat-lbl">Net Saved</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">{score}/100</span>
                <span class="fv-hero-stat-lbl">Health Score</span>
            </div>
            <div class="fv-hero-stat">
                <span class="fv-hero-stat-val">{_savings_pct:.1f}%</span>
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

    _inc_spark = _mini_spark(_monthly_inc["Amount_INR"].tolist(), "#0a7c42")
    _exp_spark = _mini_spark(_monthly_exp["Amount_INR"].tolist(), "#c0392b")
    _sav_spark = _mini_spark(_monthly_sav["sav"].tolist() if not _monthly_sav.empty else [], "#f47920")
    _score_history = [score]  # single point placeholder

    st.markdown(f'''<div class="fv-kpi-grid">
        <div class="fv-kpi-card fv-kpi-income">
            <div class="fv-kpi-tag" style="background:rgba(0,200,122,0.1);color:#00c87a;">INCOME</div>
            <div class="fv-kpi-val" style="color:#00c87a;">₹{total_inc:,.0f}</div>
            <div class="fv-kpi-label">Total Income</div>
            <div class="fv-sparkline">{_inc_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-expense">
            <div class="fv-kpi-tag" style="background:rgba(255,64,64,0.1);color:#ff4040;">EXPENSE</div>
            <div class="fv-kpi-val" style="color:#ff4040;">₹{total_exp:,.0f}</div>
            <div class="fv-kpi-label">Total Spent</div>
            <div class="fv-sparkline">{_exp_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-savings">
            <div class="fv-kpi-tag" style="background:rgba(244,121,32,0.1);color:#f47920;">SAVINGS</div>
            <div class="fv-kpi-val" style="color:#f47920;">₹{savings:,.0f}</div>
            <div class="fv-kpi-label">Net Saved</div>
            <div class="fv-sparkline">{_sav_spark}</div>
        </div>
        <div class="fv-kpi-card fv-kpi-score">
            <div class="fv-kpi-tag" style="background:rgba(26,86,255,0.1);color:#6496ff;">SCORE</div>
            <div class="fv-kpi-val" style="color:#6496ff;">{score}<span style="font-size:1rem;color:#3a4260;">/100</span></div>
            <div class="fv-kpi-label">Health Score</div>
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
# ── ADVANCED ANALYTICS (V2.0) ──
# ─────────────────────────────────────────
elif menu == "📅 Advanced Analytics":
    page_header("Advanced Analytics", "// v2.0 · time-based financial intelligence")

    df = load_transactions(st.session_state.user_id)
    if df.empty:
        st.info("No transactions yet. Add some to unlock analytics.")
        st.stop()

    today      = date.today()
    today_dt   = pd.Timestamp(today)

    # ── Auto-refresh state on 1st of month ──
    month_key = today.strftime("%Y-%m")
    if st.session_state.get("_analytics_month") != month_key:
        st.session_state["_analytics_month"] = month_key
        st.cache_data.clear()

    # ── Time window selector ──
    st.markdown("""<div class="section-tag">TIME WINDOW</div>""", unsafe_allow_html=True)
    win_col1, win_col2 = st.columns([3, 1])
    with win_col1:
        window = st.radio(
            "Analysis period",
            ["7 Days", "30 Days", "This Month", "Last Month", "All Time"],
            horizontal=True, label_visibility="collapsed"
        )
    with win_col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Filter df by window
    if window == "7 Days":
        cutoff = today_dt - pd.Timedelta(days=7)
        wdf = df[df["Date"] >= cutoff].copy()
        win_label = "Last 7 Days"
    elif window == "30 Days":
        cutoff = today_dt - pd.Timedelta(days=30)
        wdf = df[df["Date"] >= cutoff].copy()
        win_label = "Last 30 Days"
    elif window == "This Month":
        wdf = df[(df["Date"].dt.year == today.year) & (df["Date"].dt.month == today.month)].copy()
        win_label = today.strftime("%B %Y")
    elif window == "Last Month":
        lm = (today.replace(day=1) - pd.Timedelta(days=1))
        wdf = df[(df["Date"].dt.year == lm.year) & (df["Date"].dt.month == lm.month)].copy()
        win_label = lm.strftime("%B %Y")
    else:
        wdf = df.copy()
        win_label = "All Time"

    if wdf.empty:
        st.warning(f"No transactions in this window ({win_label}).")
        st.stop()

    wdf_exp = wdf[wdf["Type"] == "Expense"]
    wdf_inc = wdf[wdf["Type"] == "Income"]

    # ── New Dashboard Metrics ──
    st.markdown(f"""<div class="fv-section-title" style="margin-top:1rem;">📊 key metrics · {win_label}</div>""", unsafe_allow_html=True)

    total_inc_w  = wdf_inc["Amount_INR"].sum()
    total_exp_w  = wdf_exp["Amount_INR"].sum()
    net_savings_w = total_inc_w - total_exp_w
    n_days       = max(1, (wdf["Date"].max() - wdf["Date"].min()).days + 1)
    avg_daily_exp = total_exp_w / n_days
    avg_daily_sav = net_savings_w / n_days

    # Highest spending day
    if not wdf_exp.empty:
        daily_exp_sum = wdf_exp.groupby(wdf_exp["Date"].dt.date)["Amount_INR"].sum()
        hsd_day   = daily_exp_sum.idxmax()
        hsd_amt   = daily_exp_sum.max()
    else:
        hsd_day, hsd_amt = today, 0

    # Highest income day
    if not wdf_inc.empty:
        daily_inc_sum = wdf_inc.groupby(wdf_inc["Date"].dt.date)["Amount_INR"].sum()
        hid_day   = daily_inc_sum.idxmax()
        hid_amt   = daily_inc_sum.max()
    else:
        hid_day, hid_amt = today, 0

    st.markdown(f"""<div class="fv-kpi-grid" style="grid-template-columns:repeat(4,1fr);">
        <div class="fv-kpi-card">
            <div class="fv-kpi-tag" style="background:rgba(255,64,64,0.1);color:#ff4040;">PEAK EXPENSE DAY</div>
            <div class="fv-kpi-val" style="color:#ff4040;font-size:1.1rem;">₹{hsd_amt:,.0f}</div>
            <div class="fv-kpi-label">{hsd_day.strftime('%d %b') if hsd_amt > 0 else '—'}</div>
        </div>
        <div class="fv-kpi-card">
            <div class="fv-kpi-tag" style="background:rgba(0,200,122,0.1);color:#00c87a;">PEAK INCOME DAY</div>
            <div class="fv-kpi-val" style="color:#00c87a;font-size:1.1rem;">₹{hid_amt:,.0f}</div>
            <div class="fv-kpi-label">{hid_day.strftime('%d %b') if hid_amt > 0 else '—'}</div>
        </div>
        <div class="fv-kpi-card">
            <div class="fv-kpi-tag" style="background:rgba(244,121,32,0.1);color:#f47920;">AVG DAILY EXPENSE</div>
            <div class="fv-kpi-val" style="color:#f47920;font-size:1.1rem;">₹{avg_daily_exp:,.0f}</div>
            <div class="fv-kpi-label">per day</div>
        </div>
        <div class="fv-kpi-card">
            <div class="fv-kpi-tag" style="background:rgba(26,86,255,0.1);color:#6496ff;">AVG DAILY SAVINGS</div>
            <div class="fv-kpi-val" style="color:{'#00c87a' if avg_daily_sav>=0 else '#ff4040'};font-size:1.1rem;">₹{avg_daily_sav:,.0f}</div>
            <div class="fv-kpi-label">per day</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════
    # DAY-WISE INCOME & EXPENSE
    # ══════════════════════════════
    st.markdown("""<div class="section-tag">DAY-WISE</div>
    <div class="fv-section-title">income & expense by day 📆</div>""", unsafe_allow_html=True)

    daily_inc_d = wdf_inc.groupby(wdf_inc["Date"].dt.date)["Amount_INR"].sum().reset_index()
    daily_exp_d = wdf_exp.groupby(wdf_exp["Date"].dt.date)["Amount_INR"].sum().reset_index()
    daily_inc_d.columns = ["Date", "Income"]
    daily_exp_d.columns = ["Date", "Expense"]

    # Build full date range
    if not wdf.empty:
        all_dates = pd.DataFrame({"Date": pd.date_range(wdf["Date"].min().date(), wdf["Date"].max().date())})
        all_dates["Date"] = all_dates["Date"].dt.date
        daily_combined = all_dates.merge(daily_inc_d, on="Date", how="left") \
                                  .merge(daily_exp_d, on="Date", how="left").fillna(0)

        fig_daily = go.Figure()
        fig_daily.add_trace(go.Bar(
            x=daily_combined["Date"].astype(str), y=daily_combined["Income"],
            name="💚 Income", marker=dict(color=GREEN, opacity=0.85, line_width=0, cornerradius=4),
            hovertemplate="<b>%{x}</b><br>Income: ₹%{y:,.0f}<extra></extra>",
        ))
        fig_daily.add_trace(go.Bar(
            x=daily_combined["Date"].astype(str), y=daily_combined["Expense"],
            name="🔴 Expense", marker=dict(color=RED, opacity=0.85, line_width=0, cornerradius=4),
            hovertemplate="<b>%{x}</b><br>Expense: ₹%{y:,.0f}<extra></extra>",
        ))
        # Today marker
        fig_daily.add_vline(
            x=str(today), line_color=CYAN, line_dash="dot", line_width=1.5,
            annotation_text="today", annotation_font_color=CYAN, annotation_font_size=9
        )
        lay_d = plotly_base(280)
        lay_d.update(barmode="group", bargap=0.25,
                     xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                                tickfont=dict(size=9), tickangle=-45, nticks=12),
                     yaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                                tickprefix="₹", tickfont=dict(size=9)))
        fig_daily.update_layout(**lay_d)
        st.plotly_chart(fig_daily, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════
    # WEEK-WISE SPENDING
    # ══════════════════════════════
    st.markdown("""<div class="section-tag">WEEK-WISE</div>
    <div class="fv-section-title">weekly spending pattern 📊</div>""", unsafe_allow_html=True)

    wdf2 = wdf.copy()
    wdf2["Week"] = wdf2["Date"].dt.to_period("W").apply(lambda x: x.start_time.strftime("W of %d %b"))
    wdf2["WeekSort"] = wdf2["Date"].dt.to_period("W").astype(str)
    weekly = wdf2.groupby(["WeekSort", "Week", "Type"])["Amount_INR"].sum().reset_index()
    weekly = weekly.sort_values("WeekSort")
    weekly_p = weekly.pivot_table(index=["Week", "WeekSort"], columns="Type", values="Amount_INR", fill_value=0).reset_index()
    weekly_p = weekly_p.sort_values("WeekSort")

    if not weekly_p.empty:
        wk_labels = weekly_p["Week"].tolist()
        wk_inc = weekly_p.get("Income", pd.Series([0]*len(weekly_p))).tolist()
        wk_exp = weekly_p.get("Expense", pd.Series([0]*len(weekly_p))).tolist()
        wk_net = [i - e for i, e in zip(wk_inc, wk_exp)]

        fig_week = go.Figure()
        fig_week.add_trace(go.Bar(x=wk_labels, y=wk_inc, name="💚 Income",
            marker=dict(color=GREEN, opacity=0.85, line_width=0, cornerradius=5),
            hovertemplate="<b>%{x}</b><br>Income ₹%{y:,.0f}<extra></extra>"))
        fig_week.add_trace(go.Bar(x=wk_labels, y=wk_exp, name="🔴 Expense",
            marker=dict(color=RED, opacity=0.85, line_width=0, cornerradius=5),
            hovertemplate="<b>%{x}</b><br>Expense ₹%{y:,.0f}<extra></extra>"))
        fig_week.add_trace(go.Scatter(x=wk_labels, y=wk_net, name="✨ Net",
            mode="lines+markers",
            line=dict(color=GOLD, width=2.5, dash="dot"),
            marker=dict(size=8, color=GOLD, line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Net ₹%{y:,.0f}<extra></extra>"))
        lay_w = plotly_base(280)
        lay_w.update(barmode="group", bargap=0.28,
                     xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                                tickfont=dict(size=9), tickangle=-20),
                     yaxis=dict(gridcolor=GRID, showline=False, zeroline=True,
                                zerolinecolor="rgba(255,255,255,0.08)",
                                tickprefix="₹", tickfont=dict(size=9)))
        fig_week.update_layout(**lay_w)
        st.plotly_chart(fig_week, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════
    # MONTH-WISE COMPARISON
    # ══════════════════════════════
    st.markdown("""<div class="section-tag">MONTH-WISE</div>
    <div class="fv-section-title">month-by-month comparison 📈</div>""", unsafe_allow_html=True)

    # Always use full df for monthly comparison (not windowed)
    df_m = df.copy()
    df_m["Month"]     = df_m["Date"].dt.strftime("%b %Y")
    df_m["MonthSort"] = df_m["Date"].dt.to_period("M").astype(str)
    monthly_r = df_m.groupby(["Month", "MonthSort", "Type"])["Amount_INR"].sum().reset_index()
    monthly_r = monthly_r.sort_values("MonthSort")
    monthly_p = monthly_r.pivot_table(index=["Month","MonthSort"], columns="Type", values="Amount_INR", fill_value=0).reset_index()
    monthly_p = monthly_p.sort_values("MonthSort")

    if not monthly_p.empty:
        m_labels = monthly_p["Month"].tolist()
        m_inc    = monthly_p.get("Income", pd.Series([0]*len(monthly_p))).tolist()
        m_exp    = monthly_p.get("Expense", pd.Series([0]*len(monthly_p))).tolist()
        m_net    = [i - e for i, e in zip(m_inc, m_exp)]
        m_sr     = [round(n/i*100, 1) if i > 0 else 0 for i, n in zip(m_inc, m_net)]

        col_mv1, col_mv2 = st.columns(2)

        with col_mv1:
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Bar(x=m_labels, y=m_inc, name="💚 Income",
                marker=dict(color=GREEN, opacity=0.85, line_width=0, cornerradius=5),
                hovertemplate="<b>%{x}</b><br>Income ₹%{y:,.0f}<extra></extra>"))
            fig_mc.add_trace(go.Bar(x=m_labels, y=m_exp, name="🔴 Expense",
                marker=dict(color=RED, opacity=0.85, line_width=0, cornerradius=5),
                hovertemplate="<b>%{x}</b><br>Expense ₹%{y:,.0f}<extra></extra>"))
            lay_mc = plotly_base(260)
            lay_mc.update(barmode="group", bargap=0.28,
                          xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                                     tickfont=dict(size=9), tickangle=-30),
                          yaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                                     tickprefix="₹", tickfont=dict(size=9)),
                          title=dict(text="Income vs Expense", font=dict(size=11, color=FONT_C), x=0.5))
            fig_mc.update_layout(**lay_mc)
            st.plotly_chart(fig_mc, use_container_width=True, config={"displayModeBar": False})

        with col_mv2:
            bar_colors_net = [GREEN if v >= 0 else RED for v in m_net]
            fig_mn = go.Figure()
            fig_mn.add_trace(go.Bar(x=m_labels, y=m_net, name="✨ Net Savings",
                marker=dict(color=bar_colors_net, opacity=0.9, line_width=0, cornerradius=5),
                hovertemplate="<b>%{x}</b><br>Net ₹%{y:,.0f}<extra></extra>"))
            fig_mn.add_trace(go.Scatter(x=m_labels, y=m_sr, name="📊 Savings %",
                mode="lines+markers", yaxis="y2",
                line=dict(color=CYAN, width=2, dash="dot"),
                marker=dict(size=7, color=CYAN, line=dict(color=BG, width=1)),
                hovertemplate="<b>%{x}</b><br>Savings rate %{y:.1f}%<extra></extra>"))
            lay_mn = plotly_base(260)
            lay_mn.update(
                barmode="group", bargap=0.3,
                xaxis=dict(gridcolor=GRID, showline=False, zeroline=False,
                           tickfont=dict(size=9), tickangle=-30),
                yaxis=dict(gridcolor=GRID, showline=False, zeroline=True,
                           zerolinecolor="rgba(255,255,255,0.08)",
                           tickprefix="₹", tickfont=dict(size=9)),
                yaxis2=dict(overlaying="y", side="right", showgrid=False,
                            ticksuffix="%", tickfont=dict(size=9, color=CYAN),
                            zeroline=False),
                title=dict(text="Net Savings + Savings Rate", font=dict(size=11, color=FONT_C), x=0.5)
            )
            fig_mn.update_layout(**lay_mn)
            st.plotly_chart(fig_mn, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════
    # 7-DAY vs 30-DAY ANALYSIS TABLE
    # ══════════════════════════════
    st.markdown("""<div class="section-tag">PERIOD ANALYSIS</div>
    <div class="fv-section-title">7-day · 30-day · monthly snapshot 🔍</div>""", unsafe_allow_html=True)

    def period_stats(days):
        cut = today_dt - pd.Timedelta(days=days)
        pf  = df[df["Date"] >= cut]
        inc = pf[pf["Type"]=="Income"]["Amount_INR"].sum()
        exp = pf[pf["Type"]=="Expense"]["Amount_INR"].sum()
        return inc, exp, inc - exp

    p7_inc,  p7_exp,  p7_net  = period_stats(7)
    p30_inc, p30_exp, p30_net = period_stats(30)

    this_m_df = df[(df["Date"].dt.year==today.year)&(df["Date"].dt.month==today.month)]
    pm_inc = this_m_df[this_m_df["Type"]=="Income"]["Amount_INR"].sum()
    pm_exp = this_m_df[this_m_df["Type"]=="Expense"]["Amount_INR"].sum()
    pm_net = pm_inc - pm_exp

    col_p1, col_p2, col_p3 = st.columns(3)
    for col, label, inc, exp, net, icon in [
        (col_p1, "Last 7 Days",    p7_inc,  p7_exp,  p7_net,  "📆"),
        (col_p2, "Last 30 Days",   p30_inc, p30_exp, p30_net, "📅"),
        (col_p3, today.strftime("%B"), pm_inc, pm_exp, pm_net, "🗓️"),
    ]:
        nc = GREEN if net >= 0 else RED
        col.markdown(f"""<div class="glass-card">
            <div style="font-family:'DM Mono',monospace;font-size:0.68rem;
                letter-spacing:0.1em;color:#6a7590;text-transform:uppercase;margin-bottom:8px;">
                {icon} {label}</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:0.78rem;color:#6a7590;">Income</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.82rem;color:{GREEN};">₹{inc:,.0f}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:0.78rem;color:#6a7590;">Expense</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.82rem;color:{RED};">₹{exp:,.0f}</span>
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.06);margin:8px 0;"></div>
            <div style="display:flex;justify-content:space-between;">
                <span style="font-size:0.78rem;color:#6a7590;">Net</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.92rem;
                    font-weight:700;color:{nc};">₹{net:,.0f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ── ADD TRANSACTION ──
# ─────────────────────────────────────────
elif menu == "➕ Add Transaction":
    page_header("Add Transaction", "// log your money moves")

    PM_ICONS = {
        "Cash":"💵","UPI":"📱","Credit Card":"💳","Debit Card":"🏧",
        "Net Banking":"🏦","Cheque":"📝","EMI":"📅","Wallet":"👛","Crypto":"🪙"
    }
    payment_modes = list(PM_ICONS.keys())

    with st.form("add_tx"):
        col1, col2 = st.columns(2)
        tx_type  = col1.selectbox("Transaction Type", ["Income","Expense"])
        category = col2.text_input("Category", placeholder="e.g. Salary, Food, Rent")
        col3, col4 = st.columns([2,1])
        amount   = col3.number_input("Amount", min_value=0.01, step=0.01, value=100.0)
        currency = col4.selectbox("Currency", list(CURRENCY_RATES.keys()))
        rate       = CURRENCY_RATES[currency]
        amount_inr = amount * rate
        cur_code   = currency.split()[0]
        col5, col6 = st.columns(2)
        payment_mode = col5.selectbox("Payment Mode",
                                       [f"{PM_ICONS[m]}  {m}" for m in payment_modes])
        payment_mode_clean = payment_mode.split("  ", 1)[-1]
        tx_date = col6.date_input("Date", value=date.today())
        description = st.text_area("Note (optional)", height=70, placeholder="What was this for?")
        col7, col8 = st.columns([1,2])
        is_rec   = col7.checkbox("Recurring")
        rec_freq = col8.selectbox("Frequency", ["Monthly","Weekly","Yearly"]) if is_rec else ""
        submitted = st.form_submit_button("Log Transaction", use_container_width=True)

    if submitted:
        if not category:
            st.warning("Enter a category.")
        else:
            sb_insert("transactions", {
                "user_id": st.session_state.user_id, "type": tx_type,
                "category": category, "amount": amount, "date": str(tx_date),
                "description": description, "is_recurring": int(is_rec),
                "recur_freq": rec_freq, "currency": cur_code, "amount_inr": amount_inr,
                "payment_mode": payment_mode_clean
            })
            st.success(f"Logged {tx_type}: {category} - Rs{amount_inr:,.2f} via {payment_mode_clean}")
            st.rerun()


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
        st.dataframe(disp[[c for c in ["ID","Type","Category","Amount","Currency","Payment_Mode","Date","Description"] if c in disp.columns]],
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
            fill_color = "#c0392b" if over else "#f47920" if warn else "linear-gradient(90deg,#0a7c42,#003399)"
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
    st.dataframe(disp[[c for c in ["ID","Type","Category","Amount","Currency","Payment_Mode","Date","Description"] if c in disp.columns]],
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

        done_badge = '<span class="kpi-pill kpi-pill-green" style="margin-left:8px;">DONE</span>' if done else ""
        status_txt = "Achieved!" if done else f"{days_left}d left &nbsp;·&nbsp; Rs{remain:,.0f} to go"
        goal_html = (
            '<div class="glass-card">'
            '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
            f'<span style="font-size:1.4rem;">{gicon}</span>'
            f'<span style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#e8edf8;">{gname}</span>'
            f'{done_badge}</div>'
            f'<div style="text-align:right;min-width:130px;">'
            f'<div style="font-family:DM Mono,monospace;font-size:1.05rem;font-weight:500;color:{fill};">'
            f'Rs{gsaved:,.0f} <span style="color:#555;font-size:0.78rem;">/ Rs{gtarget:,.0f}</span></div>'
            f'<div style="font-size:0.7rem;color:#666;font-family:DM Mono,monospace;">{status_txt}</div>'
            '</div></div>'
            '<div class="budget-bar-bg">'
            f'<div class="budget-bar-fill" style="width:{pct:.1f}%;background:{fill};box-shadow:0 0 8px {fill}44;"></div>'
            '</div>'
            f'<div style="font-size:0.7rem;color:#555;font-family:DM Mono,monospace;'
            'display:flex;justify-content:space-between;margin-top:4px;">'
            f'<span>{pct:.1f}% complete</span><span>deadline {gdeadline}</span>'
            '</div></div>'
        )
        st.markdown(goal_html, unsafe_allow_html=True)

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
        _bill_layout = plotly_base(max(200, len(bills)*45))
        _bill_layout["xaxis"] = dict(
            gridcolor=GRID, showline=False, zeroline=False,
            tickfont=dict(size=10), title="Day of month", range=[0, 32]
        )
        fig_b.update_layout(**_bill_layout)
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