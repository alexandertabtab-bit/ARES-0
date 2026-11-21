# AI Model Report — ARES Prototype

## 1. Objective

The AI component of ARES is intended to help organize information from industrial inspections and support early awareness of abnormal conditions.

The project separates visual detection from sensor anomaly detection. These tasks require different data and different evaluation methods.

## 2. Computer vision: fire and smoke

**Proposed method:** YOLO object detection, starting with a lightweight model such as YOLO11n.

**Target classes:** visible fire and visible smoke. A person-detection class may be considered only if the dataset, privacy requirements, and use case support it.

**Important:** a general pretrained YOLO checkpoint is not evidence of fire/smoke detection. A task-specific model requires:
1. legally usable images representative of the intended environments;
2. bounding-box annotations for each target class;
3. train/validation/test separation;
4. evaluation on unseen images and different lighting, camera angles, and environments;
5. reporting precision, recall, and mAP, plus known failure cases.

No trained fire/smoke model or measured performance is claimed by this repository.

## 3. Sensor anomaly detection

**Prototype method:** transparent threshold-based checks on simulated temperature, vibration, electrical, and gas-alert values.

This is a baseline demonstration, not a trained predictive-maintenance model. In a later version, a model such as Isolation Forest, Random Forest, or XGBoost could be evaluated using appropriate labelled or unlabelled sensor data.

An anomaly means a reading differs from an expected range or pattern. It does **not** prove that a fire is present or will occur.

## 4. Risk indicator

The dashboard combines anomaly flags into an illustrative score and maps it to LOW, MEDIUM, or HIGH. The weights and thresholds are demonstration parameters only.

The score is not:
- a probability of fire;
- a certified industrial risk assessment;
- a substitute for engineering analysis or site-specific safety procedures.

## 5. Evaluation plan

For a future trained vision model:
- precision: how many predicted detections are correct;
- recall: how many labelled objects are detected;
- mAP50 and mAP50-95;
- confusion matrix and examples of false positives/false negatives;
- tests on unseen facilities and camera conditions.

For sensor analysis:
- compare flags against verified incident/fault labels;
- report precision, recall, false-alarm rate, and missed-event rate;
- evaluate across different machine types and operating conditions;
- prevent data leakage between training and test sets.

## 6. Data limitations

Synthetic readings are useful for demonstrating software flow but cannot establish real-world accuracy. Machine-failure datasets, including predictive-maintenance datasets, do not automatically provide fire labels. Fire-risk claims require fire-relevant, time-stamped, representative data and expert validation.

## 7. Conclusion

The current ARES repository demonstrates a transparent sensor-alert and risk-visualization workflow. Task-specific fire/smoke computer vision and validated fire-risk prediction remain development tasks, not completed capabilities.
