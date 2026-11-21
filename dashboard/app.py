import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import plotly.express as px
from simulation.factory_data import get_factory_data
from src.sensor_analysis import analyze_readings
from src.risk_engine import calculate_risk

st.set_page_config(page_title="ARES | Industrial Safety", page_icon="🚁", layout="wide")

st.title("ARES")
st.subheader("Aerial Risk Evaluation & Emergency System")
st.caption("Industrial safety monitoring prototype • Demonstration data only")

st.info(
    "This dashboard uses synthetic readings. Its anomaly flags and risk levels are "
    "for demonstration, not certified alarms or validated fire predictions."
)

df = get_factory_data()
analysis = []
for _, row in df.iterrows():
    flags = analyze_readings(row.to_dict())
    risk = calculate_risk(flags)
    analysis.append({
        **flags,
        "risk_score": risk["score"],
        "risk_level": risk["level"],
        "risk_note": risk["label"],
    })

results = df.join(__import__("pandas").DataFrame(analysis))

high_count = int((results["risk_level"] == "HIGH").sum())
medium_count = int((results["risk_level"] == "MEDIUM").sum())
normal_count = int((results["risk_level"] == "LOW").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Machines monitored", len(results))
c2.metric("High indicator", high_count)
c3.metric("Medium indicator", medium_count)
c4.metric("Low indicator", normal_count)

st.divider()
left, right = st.columns([1.25, 1])

with left:
    st.markdown("### Facility risk map")
    fig = px.scatter(
        results, x="x", y="y", color="risk_level", size="risk_score",
        hover_name="machine_id",
        hover_data=["machine", "zone", "risk_score"],
        text="machine_id",
        title="Illustrative machine locations (not a real facility layout)"
    )
    fig.update_layout(xaxis_title="Facility coordinate X", yaxis_title="Facility coordinate Y")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Unit status")
    st.write("**Unit A — Rapid response:** Concept / not connected")
    st.write("**Unit B — Hazard assessment:** Concept / facility data required")
    st.write("**Unit C — Continuous inspection:** Simulated sensor analysis active")
    st.write("**Unit D — Coordination:** Dashboard demonstration")

st.markdown("### Machine condition overview")
display_cols = [
    "machine_id", "machine", "zone", "temperature_c", "vibration_mm_s",
    "electrical_current_a", "gas_ppm", "risk_score", "risk_level"
]
st.dataframe(results[display_cols], use_container_width=True, hide_index=True)

st.markdown("### Alerts for human review")
for _, row in results.iterrows():
    if row["risk_level"] == "HIGH":
        st.error(f'{row["machine_id"]} — {row["machine"]}: HIGH illustrative indicator. Verify readings using approved site procedures.')
    elif row["risk_level"] == "MEDIUM":
        st.warning(f'{row["machine_id"]} — {row["machine"]}: MEDIUM illustrative indicator. Review the abnormal readings.')
    else:
        st.success(f'{row["machine_id"]} — {row["machine"]}: No demo threshold exceeded.')

st.divider()
st.caption(
    "ARES is a student prototype. It does not detect real fires in this dashboard, "
    "identify unknown chemicals, control machinery, or replace emergency services."
)
