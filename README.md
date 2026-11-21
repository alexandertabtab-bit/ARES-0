# ARES — Aerial Risk Evaluation & Emergency System

**ARES is a prototype concept for industrial fire-risk awareness and emergency coordination.** It connects aerial inspection, machine-condition monitoring, facility risk mapping, and incident coordination.

> **Prototype status:** This repository contains a working simulation/dashboard foundation and starter AI workflows. It is not a certified fire-safety system, does not replace firefighters or plant safety systems, and must not be used to make real emergency decisions.

## The problem

Industrial facilities contain machinery, electrical systems, hazardous materials, and people working in complex environments. During an incident, responders may not immediately have a clear picture of the affected area, nearby hazards, or the condition of equipment.

ARES aims to improve the information available to facility operators and emergency responders before and during an incident.

## The ARES concept: four connected units

| Unit | Main role | Information / output |
|---|---|---|
| **A — Rapid Response** | Aerial visual assessment during an incident | Visible fire/smoke observations, people-location observations, incident overview |
| **B — Hazard Assessment** | Support assessment of chemical and hazardous-material incidents | Facility hazard inventory, hazard-zone information, responder briefing |
| **C — Continuous Inspection** | Routine inspection and machine-condition monitoring | Sensor anomalies, inspection records, facility risk map |
| **D — Coordination** | Combine facility information with wider incident information | Situation overview, facility alerts, coordination support |

The key idea is the **shared information system**: Unit C builds facility knowledge before an incident; Units A and B can use relevant information during an incident; Unit D helps coordinate the overall response.

## System workflow

1. **PREVENT:** Unit C collects inspection and sensor information.
2. **UNDERSTAND:** The platform organizes machine conditions, locations, and known hazards.
3. **RESPOND:** Units A and B provide aerial observations and hazard-assessment support.
4. **COORDINATE:** Unit D combines available information for incident-centre awareness.

## AI approach

ARES is designed as a modular system. The prototype separates these tasks:

- **Computer vision (planned):** a YOLO model can be trained to detect visible fire and smoke in images or video. A pretrained general YOLO model does not automatically provide reliable fire/smoke detection; a task-specific dataset and evaluation are required.
- **Sensor anomaly detection (starter prototype):** identifies unusual machine readings. An anomaly is not proof that a fire will occur.
- **Risk assessment (illustrative):** combines available alerts into a transparent LOW / MEDIUM / HIGH indicator. This is a demonstration score, not a calibrated probability of fire.
- **Coordination logic (prototype):** displays facility alerts and incident information for human review.

## Prototype included in this repository

- Streamlit dashboard
- Simulated industrial facility and machine sensor readings
- Transparent anomaly checks and illustrative risk scoring
- Facility risk table and location plot
- YOLO training guide for a future fire/smoke dataset
- AI model documentation and safety limitations

## Run locally

Python 3.10 or 3.11 is recommended.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Launch the dashboard:
```bash
streamlit run dashboard/app.py
```

The dashboard uses simulated data by default. It does not require a physical drone or live sensors.

## Repository structure

```text
ARES-Intelligent-Industrial-Safety/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── docs/
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── AI_MODEL_REPORT.md
│   └── SAFETY_AND_LIMITATIONS.md
├── notebooks/
│   └── YOLO_TRAINING_GUIDE.md
├── src/
│   ├── __init__.py
│   ├── risk_engine.py
│   └── sensor_analysis.py
├── simulation/
│   ├── __init__.py
│   └── factory_data.py
└── dashboard/
    └── app.py
```

## Current limitations and next steps

- Connect real, calibrated industrial sensors.
- Collect and annotate representative fire/smoke images.
- Train and evaluate a task-specific visual model on data separated into training, validation, and test sets.
- Validate sensor-anomaly methods on representative real-world data.
- Integrate verified facility layouts and safety data sheets.
- Test communication, navigation, payload, battery, and environmental constraints.
- Conduct safety reviews with qualified industrial-safety and emergency-response professionals.

## Team

Add your team members' names and roles here before submission.

## Disclaimer

ARES is a student innovation prototype. All dashboard readings are simulated unless explicitly stated otherwise. Risk indicators are decision-support demonstrations only. They are not certified alarms, fire predictions, chemical identifications, or instructions to approach, suppress, or enter a hazardous area.
