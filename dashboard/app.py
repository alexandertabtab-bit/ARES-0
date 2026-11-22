import sys
import importlib.util
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

factory_path = ROOT / "simulation" / "factory_data.py"
factory_spec = importlib.util.spec_from_file_location("ares_factory_data", factory_path)
factory_module = importlib.util.module_from_spec(factory_spec)
factory_spec.loader.exec_module(factory_module)

get_factory_data = factory_module.get_factory_data
from src.sensor_analysis import analyze_readings
from src.risk_engine import calculate_risk

st.set_page_config(page_title="ARES | Command Center", page_icon="🚨",
                   layout="wide", initial_sidebar_state="expanded")

RED, AMBER, GREEN, CYAN, MUTED = "#F05B62", "#F2B84B", "#29C78B", "#27D8E8", "#8FA3BA"
LEVEL_COLORS = {"HIGH": RED, "MEDIUM": AMBER, "LOW": GREEN}


def html(s):
    """Render HTML without markdown treating indented lines as code."""
    st.markdown("\n".join(l.strip() for l in s.splitlines()), unsafe_allow_html=True)


def style_fig(fig, height=380):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#C7D5E5", family="Inter"),
        margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig


# ------------------------------ THEME ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#080E18;--panel:#101B2A;--border:#26384D;--cyan:#27D8E8;--text:#EDF4FC;--muted:#8FA3BA;
--red:#F05B62;--amber:#F2B84B;--green:#29C78B;}
.stApp{background:radial-gradient(1200px 600px at 80% -10%,#12304a55,transparent),var(--bg);
color:var(--text);font-family:'Inter',sans-serif;}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stSidebar"]{background:#0C1624;border-right:1px solid var(--border);}
h1,h2,h3,h4{color:var(--text)!important;font-family:'Inter',sans-serif!important;}
p,label,.stCaption{color:var(--muted);}
.block-container{padding-top:1.6rem;padding-bottom:3rem;max-width:1600px;}

.ares-topbar{display:flex;justify-content:space-between;align-items:center;background:#101D2D;
border:1px solid var(--border);border-radius:12px;padding:12px 20px;margin-bottom:18px;}
.ares-brand{color:var(--cyan);font-size:12px;font-weight:800;letter-spacing:3px;}
.ares-live{color:var(--green);font-size:11px;font-weight:700;letter-spacing:1px;}
.ares-live span{animation:pulse 1.6s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}

.ares-hero{background:linear-gradient(115deg,#173553 0%,#102033 55%,#0D1928 100%);
border:1px solid #29445E;border-radius:16px;padding:26px 30px;margin-bottom:22px;
position:relative;overflow:hidden;}
.ares-hero:after{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;
border-radius:50%;background:radial-gradient(circle,#27D8E833,transparent 70%);}
.ares-eyebrow{color:var(--cyan);font-size:11px;font-weight:800;letter-spacing:2.5px;margin-bottom:8px;}
.ares-hero-title{color:#F4F8FD;font-size:30px;font-weight:800;letter-spacing:-1px;margin-bottom:6px;}
.ares-hero-sub{color:#A9BCD0;font-size:13px;}

.ares-section{color:#EAF2FB;font-size:16px;font-weight:700;margin:6px 0 12px;}
.ares-card{background:linear-gradient(180deg,#121f31,#0f1a29);border:1px solid var(--border);
border-radius:13px;padding:16px 18px;min-height:112px;border-top:3px solid var(--accent,#27D8E8);}
.ares-card-label{color:#91A6BC;font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;}
.ares-card-value{color:#F4F8FD;font-size:30px;font-weight:800;margin-top:8px;}
.ares-card-note{color:#8298AF;font-size:11px;margin-top:3px;}

.ares-unit{background:linear-gradient(180deg,#121f31,#0f1a29);border:1px solid var(--border);
border-radius:12px 12px 0 0;padding:16px;min-height:150px;border-top:3px solid var(--accent,#27D8E8);}
.ares-unit.selected{border-color:var(--cyan);box-shadow:0 0 0 1px var(--cyan),0 8px 28px #27D8E822;}
.ares-unit-code{color:var(--cyan);font-size:12px;font-weight:800;letter-spacing:2px;}
.ares-unit-name{color:#EDF4FC;font-size:16px;font-weight:700;margin-top:8px;}
.ares-unit-desc{color:#91A6BC;font-size:11px;margin-top:5px;min-height:30px;}
.ares-unit-status{font-size:10px;font-weight:800;letter-spacing:1px;margin-top:10px;}

.ares-detail{background:#0f1a29;border:1px solid var(--cyan);border-radius:14px;padding:20px 24px;margin:14px 0;}
.ares-chip{display:inline-block;padding:3px 10px;border-radius:99px;font-size:10px;font-weight:800;
letter-spacing:1px;border:1px solid currentColor;margin-right:6px;}

div[data-testid="stPlotlyChart"]{background:var(--panel);border:1px solid var(--border);
border-radius:13px;padding:8px;}
[data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:10px;}
.stButton>button{border-radius:0 0 10px 10px;border:1px solid #267D91;background:#12394A;
color:#EAFBFF;font-weight:600;width:100%;}
.stButton>button:hover{border-color:var(--cyan);color:#fff;background:#17536A;}
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{background:#101B2A;border:1px solid var(--border);border-radius:8px;
padding:8px 16px;color:var(--muted);}
.stTabs [aria-selected="true"]{background:#12394A;color:#fff;border-color:var(--cyan);}
hr{border-color:var(--border);}
</style>
""", unsafe_allow_html=True)

# ------------------------------ STATE ------------------------------
st.session_state.setdefault("simulation_step", 0)
st.session_state.setdefault("selected_unit", None)

# ------------------------------ SIDEBAR ------------------------------
with st.sidebar:
    html("""
    <div style="padding:12px 3px 20px">
      <div style="color:#27D8E8;font-size:12px;font-weight:800;letter-spacing:3px">ARES SYSTEMS</div>
      <div style="color:#F1F6FC;font-size:27px;font-weight:800;letter-spacing:-1px">COMMAND</div>
      <div style="color:#8298AF;font-size:10px;letter-spacing:1px">INDUSTRIAL SAFETY PLATFORM</div>
    </div>""")
    st.divider()
    st.markdown("**OPERATING SCENARIO**")
    scenario = st.selectbox("Simulation scenario", [
        "Normal operation", "Machine deterioration (M-02)",
        "Gas alert (M-04)", "Multiple anomalies"], label_visibility="collapsed")
    st.caption("Change the scenario to simulate different facility conditions.")
    st.divider()
    st.markdown("**SIMULATION CONTROLS**")
    if st.button("↻  Generate new readings", use_container_width=True, key="gen"):
        st.session_state.simulation_step += 1
    st.metric("Simulation cycle", st.session_state.simulation_step)
    st.divider()
    st.markdown("**SYSTEM CONNECTIVITY**")
    st.markdown("🟢 Unit C · Simulation running")
    st.markdown("⚪ Unit A · Not connected")
    st.markdown("⚪ Unit B · Not connected")
    st.markdown("🟡 Unit D · Prototype")
    st.divider()
    st.caption("ARES Prototype · 2026")
    st.caption("Synthetic demonstration data")

# ------------------------------ DATA ------------------------------
df = get_factory_data(scenario)
analysis = []
for _, row in df.iterrows():
    flags = analyze_readings(row.to_dict())
    risk = calculate_risk(flags)
    analysis.append({**flags, "risk_score": risk["score"],
                     "risk_level": risk["level"], "risk_note": risk["label"]})
results = df.join(pd.DataFrame(analysis))

high_count = int((results["risk_level"] == "HIGH").sum())
medium_count = int((results["risk_level"] == "MEDIUM").sum())
low_count = int((results["risk_level"] == "LOW").sum())
total = len(results)
top = results.sort_values("risk_score", ascending=False).iloc[0]

alerts = []
for _, row in results.iterrows():
    f = []
    if row["temperature_anomaly"]: f.append("High temperature")
    if row["vibration_anomaly"]: f.append("High vibration")
    if row["electrical_anomaly"]: f.append("Abnormal electrical current")
    if row["gas_alert"]: f.append("Gas threshold exceeded")
    if f:
        alerts.append((row, f))

# ------------------------------ HEADER ------------------------------
html(f"""
<div class="ares-topbar">
  <div class="ares-brand">ARES / OPERATIONS CENTER</div>
  <div class="ares-live"><span>●</span> SIMULATION ONLINE · {datetime.now():%H:%M:%S} · CYCLE {st.session_state.simulation_step}</div>
</div>
<div class="ares-hero">
  <div class="ares-eyebrow">INDUSTRIAL INTELLIGENCE NETWORK</div>
  <div class="ares-hero-title">Command Center</div>
  <div class="ares-hero-sub">Facility monitoring · Risk assessment · Emergency coordination</div>
</div>""")

# ------------------------------ KPIs ------------------------------
html('<div class="ares-section">Operational overview</div>')
kpis = [
    ("Monitoring points", f"{total:02d}", "Industrial sensor locations", CYAN, "#F4F8FD"),
    ("High indicators", f"{high_count:02d}", "Require human review", RED, RED),
    ("Medium indicators", f"{medium_count:02d}", "Conditions to investigate", AMBER, AMBER),
    ("Normal indicators", f"{low_count:02d}", "No demo threshold exceeded", GREEN, GREEN),
]
for col, (label, val, note, accent, vcolor) in zip(st.columns(4), kpis):
    with col:
        html(f"""<div class="ares-card" style="--accent:{accent}">
        <div class="ares-card-label">{label}</div>
        <div class="ares-card-value" style="color:{vcolor}">{val}</div>
        <div class="ares-card-note">{note}</div></div>""")

st.write("")

# ------------------------------ UNIT NETWORK (CLICKABLE) ------------------------------
html('<div class="ares-section">ARES unit network <span style="color:#8298AF;font-size:12px;font-weight:500">— click a unit to open it</span></div>')

units = {
    "A": ("Rapid response", "Drone response and visual assessment", "CONCEPT / NOT CONNECTED", "#8298AF"),
    "B": ("Hazard assessment", "Gas monitoring and chemical context", "CONCEPT / NOT CONNECTED", "#8298AF"),
    "C": ("Industrial intelligence", "Continuous sensor analysis", "SIMULATION ACTIVE", GREEN),
    "D": ("Incident coordination", "Shared incident and facility overview", "PROTOTYPE", AMBER),
}
for col, (code, (name, desc, status, color)) in zip(st.columns(4), units.items()):
    with col:
        sel = "selected" if st.session_state.selected_unit == code else ""
        html(f"""<div class="ares-unit {sel}" style="--accent:{color}">
        <div class="ares-unit-code">UNIT {code}</div>
        <div class="ares-unit-name">{name}</div>
        <div class="ares-unit-desc">{desc}</div>
        <div class="ares-unit-status" style="color:{color}">● {status}</div></div>""")
        label = "✕ Close" if sel else f"Open Unit {code}  →"
        if st.button(label, key=f"unit_{code}", use_container_width=True):
            st.session_state.selected_unit = None if sel else code
            st.rerun()

# Detail panel for the selected unit
sel_code = st.session_state.selected_unit
if sel_code:
    name, desc, status, color = units[sel_code]
    html(f"""<div class="ares-detail">
    <span class="ares-chip" style="color:{color}">{status}</span>
    <span class="ares-chip" style="color:#8FA3BA">UNIT {sel_code}</span>
    <div style="font-size:22px;font-weight:800;color:#F4F8FD;margin-top:10px">{name}</div>
    <div style="color:#A9BCD0;font-size:13px;margin-top:4px">{desc}</div></div>""")

    if sel_code == "A":
        st.info("Concept unit — not connected. In a real deployment it would be dispatched to the "
                "highest-risk location for visual assessment.")
        st.metric("Suggested dispatch target (simulated)",
                  f"{top['machine_id']} · {top['machine']}", f"{top['zone']}")
    elif sel_code == "B":
        st.info("Concept unit — not connected. Showing simulated gas readings as a preview.")
        g = px.bar(results, x="machine_id", y="gas_ppm", color="risk_level",
                   color_discrete_map=LEVEL_COLORS, title="Gas reading by machine (ppm)")
        st.plotly_chart(style_fig(g, 300), use_container_width=True)
    elif sel_code == "C":
        c1, c2, c3 = st.columns(3)
        c1.metric("Sensors analysed", total)
        c2.metric("Active alerts", len(alerts))
        c3.metric("Highest risk", f"{top['machine_id']}", f"score {top['risk_score']}")
        st.dataframe(results[["machine_id", "machine", "risk_score", "risk_level"]]
                     .sort_values("risk_score", ascending=False),
                     hide_index=True, use_container_width=True)
    else:
        st.markdown("**Incident overview**")
        if not alerts:
            st.success("No open incidents.")
        for row, f in alerts:
            (st.error if row["risk_level"] == "HIGH" else st.warning)(
                f"{row['machine_id']} — {row['machine']} · {row['zone']} | {', '.join(f)}")

st.write("")

# ------------------------------ MAIN TABS ------------------------------
tab_map, tab_sensors, tab_alerts, tab_vision = st.tabs(
    ["🗺  Facility map", "📡  Sensor intelligence", "🚨  Alerts", "👁  Vision (YOLO)"])

with tab_map:
    map_col, side_col = st.columns([1.7, 1])
    with map_col:
        fig = px.scatter(
            results, x="x", y="y", color="risk_level", size="risk_score", size_max=34,
            text="machine_id", hover_name="machine",
            hover_data={"zone": True, "temperature_c": ":.1f", "vibration_mm_s": ":.2f",
                        "risk_score": True, "x": False, "y": False},
            color_discrete_map=LEVEL_COLORS,
            category_orders={"risk_level": ["HIGH", "MEDIUM", "LOW"]})
        fig.update_traces(marker=dict(line=dict(width=2, color="#EAF4FF"), opacity=0.92),
                          textposition="top center", textfont=dict(color="#DCEAF8", size=10))
        style_fig(fig, 440)
        fig.update_layout(
            xaxis=dict(title="Facility X", gridcolor="#1c2d42", zeroline=False),
            yaxis=dict(title="Facility Y", gridcolor="#1c2d42", zeroline=False,
                       scaleanchor="x", scaleratio=1),
            legend=dict(title="RISK", orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Illustrative facility layout. Coordinates and sensor readings are simulated.")
    with side_col:
        peak = float(results["risk_score"].max())
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=peak,
            title={"text": "Peak risk score", "font": {"size": 14}},
            gauge={"axis": {"range": [0, max(100, peak)], "tickcolor": MUTED},
                   "bar": {"color": CYAN, "thickness": 0.25},
                   "bgcolor": "#0d1826", "borderwidth": 0,
                   "steps": [{"range": [0, 33], "color": "#1b4d3e"},
                             {"range": [33, 66], "color": "#5a4a1f"},
                             {"range": [66, max(100, peak)], "color": "#5a2a2e"}]}))
        st.plotly_chart(style_fig(gauge, 215), use_container_width=True)
        donut = go.Figure(go.Pie(
            labels=["HIGH", "MEDIUM", "LOW"], values=[high_count, medium_count, low_count],
            hole=0.65, marker=dict(colors=[RED, AMBER, GREEN], line=dict(color="#101B2A", width=2)),
            textinfo="none"))
        donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1),
                            title=dict(text="Risk distribution", font=dict(size=14)))
        st.plotly_chart(style_fig(donut, 215), use_container_width=True)

with tab_sensors:
    zone_df = results.groupby("zone", as_index=False)["risk_score"].max()
    zbar = px.bar(zone_df, x="zone", y="risk_score", color="risk_score",
                  color_continuous_scale=[GREEN, AMBER, RED], title="Peak risk by zone")
    zbar.update_coloraxes(showscale=False)
    st.plotly_chart(style_fig(zbar, 260), use_container_width=True)

    cols = ["machine_id", "machine", "zone", "temperature_c", "vibration_mm_s",
            "electrical_current_a", "gas_ppm", "risk_score", "risk_level"]
    st.dataframe(
        results[cols].round(2), use_container_width=True, hide_index=True,
        column_config={
            "machine_id": "ID", "machine": "Equipment", "zone": "Facility zone",
            "temperature_c": st.column_config.NumberColumn("Temperature", format="%.1f °C"),
            "vibration_mm_s": st.column_config.NumberColumn("Vibration", format="%.2f mm/s"),
            "electrical_current_a": st.column_config.NumberColumn("Current", format="%.1f A"),
            "gas_ppm": st.column_config.NumberColumn("Gas reading", format="%.1f ppm"),
            "risk_score": st.column_config.ProgressColumn(
                "Demo score", min_value=0, max_value=max(100, float(results["risk_score"].max())),
                format="%.0f"),
            "risk_level": "Indicator"})

with tab_alerts:
    if not alerts:
        st.success("No demonstration thresholds exceeded in the current scenario.")
    for row, f in alerts:
        msg = ", ".join(f)
        if row["risk_level"] == "HIGH":
            st.error(f"🔴 HIGH INDICATOR · {row['machine_id']} — {row['machine']} | {msg}")
        else:
            st.warning(f"🟠 REVIEW REQUIRED · {row['machine_id']} — {row['machine']} | {msg}")

with tab_vision:
    from PIL import Image

    st.markdown("**Visual detection (YOLO)** — upload a photo or use your camera.")
    weights = st.text_input("Weights file inside the models/ folder", value="best.pt")
    conf = st.slider("Confidence threshold", 0.05, 0.95, 0.25, 0.05)
    up = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    cam = st.camera_input("...or take a photo")
    source = up or cam

    if source is None:
        st.info("Waiting for an image.")
    else:
        try:
            from src.vision import load_model, detect

            model = load_model(weights)
            img = Image.open(source).convert("RGB")
            annotated, dets = detect(model, img, conf)

            c1, c2 = st.columns(2)
            c1.image(img, caption="Input", use_container_width=True)
            c2.image(annotated, caption="YOLO detections", use_container_width=True)

            if dets:
                st.error(f"{len(dets)} detection(s) found, human review required.")
                st.dataframe(dets, hide_index=True, use_container_width=True)
            else:
                st.success("Nothing detected above the threshold.")
        except ImportError:
            st.error("Missing package. Run: pip install ultralytics opencv-python-headless pillow")
        except FileNotFoundError as e:
            st.error(f"{e}. Check that the file is inside the models/ folder.")
        except Exception as e:
            st.error(f"Vision error: {e}")

# ------------------------------ FOOTER ------------------------------
st.divider()
html("""
<div style="text-align:center;padding:12px 5px 5px">
  <div style="color:#27D8E8;font-size:11px;font-weight:800;letter-spacing:2px">
    ARES — AERIAL RISK EVALUATION &amp; EMERGENCY SYSTEM</div>
  <div style="color:#71869D;font-size:10px;margin-top:7px">
    Student prototype · Synthetic data · Human review required</div>
  <div style="color:#71869D;font-size:10px;margin-top:4px">
    Not a certified alarm system, validated fire prediction model, or replacement for emergency services.</div>
</div>""")
