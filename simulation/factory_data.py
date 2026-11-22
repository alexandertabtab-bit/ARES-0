
"""Synthetic factory readings for ARES demonstrations only."""

import random
import pandas as pd


def get_factory_data(scenario="Normal operation"):
    """Generate simulated industrial sensor readings."""

    machines = [
        {
            "machine_id": "M-01", "machine": "Compressor",
            "zone": "Production", "x": 12, "y": 18,
            "temperature_c": 62, "vibration_mm_s": 3.2,
            "electrical_current_a": 18, "gas_ppm": 4
        },
        {
            "machine_id": "M-02", "machine": "Industrial motor",
            "zone": "Production", "x": 30, "y": 22,
            "temperature_c": 65, "vibration_mm_s": 3.5,
            "electrical_current_a": 20, "gas_ppm": 8
        },
        {
            "machine_id": "M-03", "machine": "Electrical panel",
            "zone": "Electrical room", "x": 48, "y": 15,
            "temperature_c": 55, "vibration_mm_s": 1.1,
            "electrical_current_a": 22, "gas_ppm": 3
        },
        {
            "machine_id": "M-04", "machine": "Chemical storage monitor",
            "zone": "Storage", "x": 65, "y": 42,
            "temperature_c": 58, "vibration_mm_s": 1.4,
            "electrical_current_a": 9, "gas_ppm": 8
        },
        {
            "machine_id": "M-05", "machine": "Ventilation unit",
            "zone": "Utilities", "x": 22, "y": 58,
            "temperature_c": 49, "vibration_mm_s": 2.0,
            "electrical_current_a": 12, "gas_ppm": 2
        },
    ]

    for machine in machines:
        # Small random variations to simulate changing sensor readings.
        machine["temperature_c"] += random.uniform(-2, 2)
        machine["vibration_mm_s"] += random.uniform(-0.3, 0.3)
        machine["electrical_current_a"] += random.uniform(-1.5, 1.5)
        machine["gas_ppm"] += random.uniform(-1, 1)

    # Scenario 1: one machine develops abnormal conditions.
    if scenario == "Machine deterioration (M-02)":
        target = machines[1]
        target["temperature_c"] = random.uniform(82, 90)
        target["vibration_mm_s"] = random.uniform(7.2, 9)
        target["electrical_current_a"] = random.uniform(31, 36)

    # Scenario 2: abnormal gas reading in the storage zone.
    elif scenario == "Gas alert (M-04)":
        target = machines[3]
        target["gas_ppm"] = random.uniform(55, 80)

    # Scenario 3: several machines show abnormal readings.
    elif scenario == "Multiple anomalies":
        motor = machines[1]
        motor["temperature_c"] = random.uniform(82, 90)
        motor["vibration_mm_s"] = random.uniform(7.2, 9)
        motor["electrical_current_a"] = random.uniform(31, 36)

        storage = machines[3]
        storage["gas_ppm"] = random.uniform(55, 80)

        panel = machines[2]
        panel["electrical_current_a"] = random.uniform(32, 36)

    return pd.DataFrame(machines)
