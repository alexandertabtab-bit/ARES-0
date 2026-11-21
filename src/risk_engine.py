"""Illustrative risk scoring. This is not a fire probability or certified risk model."""

def calculate_risk(flags):
    weights = {
        "temperature_anomaly": 30,
        "vibration_anomaly": 15,
        "electrical_anomaly": 25,
        "gas_alert": 30,
    }
    score = sum(weight for key, weight in weights.items() if flags.get(key, False))

    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "label": "Illustrative indicator — not a fire probability"
    }
