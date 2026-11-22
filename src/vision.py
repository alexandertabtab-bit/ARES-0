"""YOLO helper for ARES. Save this as src/vision.py"""
from pathlib import Path

import streamlit as st

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"


@st.cache_resource(show_spinner="Loading YOLO model...")
def load_model(weights_name: str = "best.pt"):
    """Load the YOLO weights once and keep them in memory."""
    from ultralytics import YOLO

    path = MODELS_DIR / weights_name
    if not path.exists():
        raise FileNotFoundError(f"Weights not found: {path}")
    return YOLO(str(path))


def detect(model, image, conf: float = 0.25):
    """Run YOLO on a PIL image or numpy array.

    Returns (annotated_rgb_image, list_of_detections).
    """
    result = model.predict(image, conf=conf, verbose=False)[0]
    annotated = result.plot()[:, :, ::-1]  # BGR -> RGB for Streamlit

    detections = []
    for box in result.boxes:
        cls_id = int(box.cls[0])
        detections.append({
            "class": result.names[cls_id],
            "confidence": round(float(box.conf[0]), 2),
            "box": [round(v) for v in box.xyxy[0].tolist()],
        })
    return annotated, detections
