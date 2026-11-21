# YOLO Fire/Smoke Training Guide (Google Colab)

This is a training plan, not evidence that a fire/smoke model has already been trained.

## 1. Prepare a dataset
Use a dataset whose license permits your use. It must contain images representative of industrial environments. Annotate bounding boxes for `fire` and `smoke` using a tool such as Roboflow or another annotation tool.

Recommended split:
- train: 70%
- validation: 20%
- test: 10%

Keep related video frames or images from the same recording in one split to reduce data leakage.

## 2. Dataset YAML

Create `fire_smoke.yaml` and update the paths to match your dataset:

```yaml
path: /content/fire_smoke_dataset
train: images/train
val: images/val
test: images/test

names:
  0: fire
  1: smoke
```

The label IDs must match the annotation export.

## 3. Colab setup

```python
!pip install -q ultralytics
import torch
from ultralytics import YOLO

print("GPU available:", torch.cuda.is_available())
```

If Colab offers a GPU, select Runtime > Change runtime type > T4 GPU.

## 4. Train a lightweight model

```python
model = YOLO("yolo11n.pt")
results = model.train(
    data="/content/fire_smoke.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    patience=10
)
```

Training settings may need to be reduced if GPU memory is limited.

## 5. Evaluate

```python
metrics = model.val(data="/content/fire_smoke.yaml")
print(metrics)
```

Record precision, recall, mAP50, and mAP50-95 from the validation/test evaluation. Do not report example results as measured results.

## 6. Test an unseen image

```python
model = YOLO("runs/detect/train/weights/best.pt")
results = model.predict(
    source="/content/test_image.jpg",
    conf=0.25,
    save=True
)
```

Inspect false positives and missed detections. Test on images not used during training.

## 7. Report honestly

Document dataset name, source, license, number of images, class counts, split method, training settings, evaluation metrics, and limitations. If training is not completed, state that it is planned work.
