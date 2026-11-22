
import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --background: #080F1B;
        --surface: #101B2D;
        --surface-light: #17263B;
        --border: #26374D;
        --cyan: #22D3EE;
        --text: #E5EDF7;
        --muted: #91A3B8;
        --red: #F05252;
        --amber: #F5B942;
        --green: #22C58B;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #0C1727;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] p {
        color: var(--text);
    }

    h1, h2, h3 {
        color: #F1F7FF !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.5px;
    }

    p, label {
        color: var(--muted);
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: #F1F7FF;
        font-weight: 700;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    div[data-testid="stPlotlyChart"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px;
    }

    .ares-header {
        background: linear-gradient(110deg, #12243A, #0D192A);
        border: 1px solid #263C55;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 22px;
    }

    .ares-eyebrow {
        color: var(--cyan);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .ares-title {
        color: #F1F7FF;
        font-size: 30px;
        font-weight: 800;
        margin: 5px 0;
    }

    .ares-subtitle {
        color: #9BAFC5;
        font-size: 13px;
    }

    .ares-panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .ares-muted {
        color: var(--muted);
        font-size: 12px;
    }

    button[kind="primary"] {
        background: #087E9A;
        border: 1px solid #22D3EE;
        color: white;
        border-radius: 8px;
    }

    button[kind="primary"]:hover {
        background: #0A9DBB;
        border-color: #67E8F9;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(unit, title, description, status="PROTOTYPE"):
    st.markdown(f"""
    <div class="ares-header">
        <div class="ares-eyebrow">ARES / {unit} / {status}</div>
        <div class="ares-title">{title}</div>
        <div class="ares-subtitle">{description}</div>
    </div>
    """, unsafe_allow_html=True)
