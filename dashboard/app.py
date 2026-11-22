
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
import plotly.express as px

from simulation.factory_data import get_factory_data
from src.sensor_analysis import analyze_readings
from src.risk_engine import calculate_risk


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="ARES | Command Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# VISUAL THEME
# ---------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080E18;
    --panel: #101B2A;
    --panel2: #142236;
    --border: #26384D;
    --cyan: #27D8E8;
    --text: #EDF4FC;
    --muted: #8FA3BA;
    --red: #F05B62;
    --amber: #F2B84B;
    --green: #29C78B;
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0C1624;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #C1D0E0;
}

h1, h2, h3, h4 {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

p, label, .stCaption {
    color: var(--muted);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

.ares-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #101D2D;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 13px 20px;
    margin-bottom: 22px;
}

.ares-brand {
    color: var(--cyan);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.ares-live {
    color: var(--green);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.ares-hero {
    background: linear-gradient(115deg, #142B42 0%, #102033 55%, #0D1928 100%);
    border: 1px solid #29445E;
    border-radius: 16px;
    padding: 27px 30px;
    margin-bottom: 22px;
}

.ares-eyebrow {
    color: var(--cyan);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.5px;
    margin-bottom: 8px;
}

.ares-hero-title {
    color: #F4F8FD;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 6px;
}

.ares-hero-sub {
    color: #A9BCD0;
    font-size: 13px;
}

.ares-section {
    color: #EAF2FB;
    font-size: 16px;
    font-weight: 700;
    margin: 8px 0 13px 0;
}

.ares-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 17px 18px;
    min-height: 112px;
}

.ares-card-label {
    color: #91A6BC;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

.ares-card-value {
    color: #F4F8FD;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}

.ares-card-note {
    color: #8298AF;
    font-size: 11px;
    margin-top: 3px;
}

.ares-unit {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    min-height: 145px;
}

.ares-unit-code {
    color: var(--cyan);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.ares-unit-name {
    color: #EDF4FC;
    font-size: 16px;
    font-weight: 700;
    margin-top: 9px;
}

.ares-unit-desc {
    color: #91A6BC;
    font-size: 11px;
    margin-top: 5px;
    min-height: 30px;
}

.ares-unit-status {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 13px;
}

div[data-testid="stPlotlyChart"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 10px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
}

.stButton > button {
    border-radius: 8px;
    border: 1px solid #267D91;
    background: #12394A;
    color: #EAFBFF;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: var(--cyan);
    color: white;
    background: #17536A;
}

hr {
    border-color: var(--border);
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 3px 20px">
        <div style="color:#27D8E8;font-size:12px;
                    font-weight:800;letter-spacing:3px">
            ARES SYSTEMS
        </div>
        <div style="color:#F1F6FC;font-size:27px;
                    font-weight:800;letter-spacing:-1px">
            COMMAND
        </div>
        <div style="color:#8298AF;font-size:10px;
                    letter-spacing:1px">
            INDUSTRIAL SAFETY PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**OPERATING SCENARIO**")

    scenario = st.selectbox(
        "Simulation scenario",
        [
            "Normal operation",
            "Machine deterioration (M-02)",
            "Gas alert (M-04)",
            "Multiple anomalies"
        ],
        label_visibility="collapsed"
    )

    st.caption("Change the scenario to simulate different facility conditions.")

    st.divider()

    st.markdown("**SIMULATION CONTROLS**")

    if "simulation_step" not in st.session_state:
        st.session_state.simulation_step = 0

    if st.button("↻  Generate new readings", use_container_width=True):
        st.session_state.simulation_step += 1

    st.metric("Simulation cycle", st.session_state.simulation_step)

    st.divider()

    st.markdown("**SYSTEM CONNECTIVITY**")
    st.markdown("🟢 Unit C · Simulation running")
    st.markdown("⚪ Unit A · Not connected")
    st.markdown("⚪ Unit B · Not connected")
    st.markdown("⚪ Unit D · Prototype")

    st.divider()
    st.caption("ARES Prototype · 2026")
    st.caption("Synthetic demonstration data")


# ---------------------------------------------------------
# DATA PROCESSING
# ---------------------------------------------------------

def get_factory_data(scenario="Normal operation"):
    analysis = []
    for _, row in df.iterrows():
        flags = analyze_readings(row.to_dict())
        risk = calculate_risk(flags)
        analysis.append({
            **flags,
            "risk_score": risk["score"],
            "risk_level": risk["level"],
            "risk_note": risk["label"]
        })
        results = df.join(pd.DataFrame(analysis))
        high_count = int((results["risk_level"] == "HIGH").sum())
        medium_count = int((results["risk_level"] == "MEDIUM").sum())
        low_count = int((results["risk_level"] == "LOW").sum())
        total = len(results)

# ---------------------------------------------------------
# TOP BAR AND HERO
# ---------------------------------------------------------

st.markdown("""
<div class="ares-topbar">
    <div class="ares-brand">ARES / OPERATIONS CENTER</div>
    <div class="ares-live">● SIMULATION ONLINE</div>
</div>

<div class="ares-hero">
    <div class="ares-eyebrow">INDUSTRIAL INTELLIGENCE NETWORK</div>
    <div class="ares-hero-title">Command Center</div>
    <div class="ares-hero-sub">
        Facility monitoring · Risk assessment · Emergency coordination
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ---------------------------------------------------------

st.markdown('<div class="ares-section">Operational overview</div>',
            unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="ares-card">
        <div class="ares-card-label">Monitoring points</div>
        <div class="ares-card-value">{total:02d}</div>
        <div class="ares-card-note">Industrial sensor locations</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="ares-card">
        <div class="ares-card-label">High indicators</div>
        <div class="ares-card-value">{high_count:02d}</div>
        <div class="ares-card-note">Require human review</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="ares-card">
        <div class="ares-card-label">Medium indicators</div>
        <div class="ares-card-value" style="color:#F2B84B">{medium_count:02d}</div>
        <div class="ares-card-note">Conditions to investigate</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="ares-card">
        <div class="ares-card-label">Normal indicators</div>
        <div class="ares-card-value" style="color:#29C78B">{low_count:02d}</div>
        <div class="ares-card-note">No demo threshold exceeded</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ---------------------------------------------------------
# FACILITY MAP AND SYSTEM STATUS
# ---------------------------------------------------------

map_col, status_col = st.columns([1.65, 1])

with map_col:
    st.markdown('<div class="ares-section">Facility intelligence map</div>',
                unsafe_allow_html=True)

    fig = px.scatter(
        results,
        x="x",
        y="y",
        color="risk_level",
        size="risk_score",
        size_max=30,
        text="machine_id",
        hover_name="machine",
        hover_data={
            "zone": True,
            "temperature_c": ":.1f",
            "vibration_mm_s": ":.2f",
            "risk_score": True,
            "x": False,
            "y": False
        },
        color_discrete_map={
            "HIGH": "#F05B62",
            "MEDIUM": "#F2B84B",
            "LOW": "#29C78B"
        },
        category_orders={
            "risk_level": ["HIGH", "MEDIUM", "LOW"]
        }
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=1.5, color="#EAF4FF"),
            opacity=0.9
        ),
        textposition="top center",
        textfont=dict(color="#DCEAF8", size=10)
    )

    fig.update_layout(
        height=410,
        paper_bgcolor="#101B2A",
        plot_bgcolor="#101B2A",
        font=dict(color="#C7D5E5", family="Inter"),
        margin=dict(l=15, r=15, t=20, b=15),
        xaxis=dict(
            title="Facility coordinate X",
            gridcolor="#26384D",
            zeroline=False
        ),
        yaxis=dict(
            title="Facility coordinate Y",
            gridcolor="#26384D",
            zeroline=False,
            scaleanchor="x",
            scaleratio=1
        ),
        legend=dict(
            title="RISK INDICATOR",
            orientation="h",
            y=-0.18
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Illustrative facility layout. Coordinates and sensor readings are simulated."
    )


with status_col:
    st.markdown('<div class="ares-section">ARES unit network</div>',
                unsafe_allow_html=True)

    unit_data = [
        ("UNIT A", "Rapid response",
         "Drone response and visual assessment",
         "CONCEPT / NOT CONNECTED", "#8298AF"),
        ("UNIT B", "Hazard assessment",
         "Gas monitoring and chemical context",
         "CONCEPT / NOT CONNECTED", "#8298AF"),
        ("UNIT C", "Industrial intelligence",
         "Continuous sensor analysis",
         "SIMULATION ACTIVE", "#29C78B"),
        ("UNIT D", "Incident coordination",
         "Shared incident and facility overview",
         "PROTOTYPE", "#F2B84B")
    ]

    for code, name, desc, status, color in unit_data:
        st.markdown(f"""
        <div class="ares-unit">
            <div class="ares-unit-code">{code}</div>
            <div class="ares-unit-name">{name}</div>
            <div class="ares-unit-desc">{desc}</div>
            <div class="ares-unit-status" style="color:{color}">
                ● {status}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")


# ---------------------------------------------------------
# SENSOR TABLE
# ---------------------------------------------------------

st.divider()

st.markdown('<div class="ares-section">Industrial sensor intelligence</div>',
            unsafe_allow_html=True)

display_cols = [
    "machine_id",
    "machine",
    "zone",
    "temperature_c",
    "vibration_mm_s",
    "electrical_current_a",
    "gas_ppm",
    "risk_score",
    "risk_level"
]

table = results[display_cols].copy()
table = table.round(2)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "machine_id": "ID",
        "machine": "Equipment",
        "zone": "Facility zone",
        "temperature_c": st.column_config.NumberColumn("Temperature", format="%.1f °C"),
        "vibration_mm_s": st.column_config.NumberColumn("Vibration", format="%.2f mm/s"),
        "electrical_current_a": st.column_config.NumberColumn("Current", format="%.1f A"),
        "gas_ppm": st.column_config.NumberColumn("Gas reading", format="%.1f ppm"),
        "risk_score": "Demo score",
        "risk_level": "Indicator"
    }
)


# ---------------------------------------------------------
# ALERT CENTER
# ---------------------------------------------------------

st.divider()

st.markdown('<div class="ares-section">Alert and review center</div>',
            unsafe_allow_html=True)

alerts = []

for _, row in results.iterrows():
    active_flags = []

    if row["temperature_anomaly"]:
        active_flags.append("High temperature")

    if row["vibration_anomaly"]:
        active_flags.append("High vibration")

    if row["electrical_anomaly"]:
        active_flags.append("Abnormal electrical current")

    if row["gas_alert"]:
        active_flags.append("Gas threshold exceeded")

    if active_flags:
        alerts.append((row, active_flags))

if not alerts:
    st.success("No demonstration thresholds exceeded in the current scenario.")

else:
    for row, active_flags in alerts:
        message = ", ".join(active_flags)

        if row["risk_level"] == "HIGH":
            st.error(
                f" HIGH INDICATOR · {row['machine_id']} — {row['machine']} | {message}"
            )
        else:
            st.warning(
                f" REVIEW REQUIRED · {row['machine_id']} — {row['machine']} | {message}"
            )


# ---------------------------------------------------------
# FOOTER / LIMITATIONS
# ---------------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center;padding:12px 5px 5px">
    <div style="color:#27D8E8;font-size:11px;
                font-weight:800;letter-spacing:2px">
        ARES — AERIAL RISK EVALUATION & EMERGENCY SYSTEM
    </div>
    <div style="color:#71869D;font-size:10px;margin-top:7px">
        Student prototype · Synthetic data · Human review required
    </div>
    <div style="color:#71869D;font-size:10px;margin-top:4px">
        Not a certified alarm system, validated fire prediction model,
        or replacement for emergency services.
    </div>
</div>
""", unsafe_allow_html=True)
