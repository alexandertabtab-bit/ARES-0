"""Transparent baseline checks for simulated industrial sensor readings."""

def analyze_readings(readings):
    """Return anomaly flags. Thresholds are illustrative demo values, not standards."""
    flags = {
        "temperature_anomaly": readings["temperature_c"] >= 80,
        "vibration_anomaly": readings["vibration_mm_s"] >= 7,
        "electrical_anomaly": readings["electrical_current_a"] >= 30,
        "gas_alert": readings["gas_ppm"] >= 50,
    }
    return flags
