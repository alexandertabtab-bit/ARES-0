"""Synthetic factory readings for dashboard demonstration only."""
import pandas as pd

def get_factory_data():
    rows = [
        {"machine_id": "M-01", "machine": "Compressor", "zone": "Production", "x": 12, "y": 18,
         "temperature_c": 62, "vibration_mm_s": 3.2, "electrical_current_a": 18, "gas_ppm": 4},
        {"machine_id": "M-02", "machine": "Industrial motor", "zone": "Production", "x": 30, "y": 22,
         "temperature_c": 86, "vibration_mm_s": 8.1, "electrical_current_a": 34, "gas_ppm": 8},
        {"machine_id": "M-03", "machine": "Electrical panel", "zone": "Electrical room", "x": 48, "y": 15,
         "temperature_c": 55, "vibration_mm_s": 1.1, "electrical_current_a": 33, "gas_ppm": 3},
        {"machine_id": "M-04", "machine": "Chemical storage monitor", "zone": "Storage", "x": 65, "y": 42,
         "temperature_c": 58, "vibration_mm_s": 1.4, "electrical_current_a": 9, "gas_ppm": 72},
        {"machine_id": "M-05", "machine": "Ventilation unit", "zone": "Utilities", "x": 22, "y": 58,
         "temperature_c": 49, "vibration_mm_s": 2.0, "electrical_current_a": 12, "gas_ppm": 2},
    ]
    return pd.DataFrame(rows)
