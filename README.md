<div align="center">

# Realtime Defect Detection

**Detect surface, weld, and paint defects from a live camera feed — in real time.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![YOLOv9](https://img.shields.io/badge/YOLOv9-Ultralytics-FF6F00?style=flat&logo=pytorch&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Overview

Realtime Defect Detection is a Flask-based computer vision application for industrial inspection. Point a camera at a surface — it runs YOLOv9 inference per frame, overlays detections, logs results to CSV, and shows live class-wise statistics.

```
Camera Feed → Frame Capture → Preprocessing → YOLOv9 Inference → Detection Overlay → CSV Log → Analytics
```

---

## Features

### Core Pipeline
- **Live Inference** — per-frame detection streamed from a webcam using YOLOv9
- **Multi-Model Support** — switch between surface, weld, and paint detection models at runtime
- **Zoom Mode** — crops a region of the frame and passes it to the model for fine-grained inspection
- **CLAHE + Sharpening** — contrast enhancement applied selectively to the weld pipeline; skipped for other models to preserve accuracy
- **Segmentation Overlay** — masks drawn directly on the live feed

### Logging and Analytics
- Every detection logged to CSV with timestamp and class label
- Live bar chart and pie chart — detection count per class, updated per session
- Stats reset on new session; CSV persists across runs

---

## Models

| Target | Architecture | Dataset | Classes |
|--------|-------------|---------|---------|
| Surface | YOLOv9c | NEU-DET | `crazing` `inclusion` `patches` `pitted_surface` `rolled-in_scale` `scratches` |
| Weld | YOLOv9c | Custom | — |
| Paint | YOLOv9c | Custom | — |

Surface model trained at 100 epochs · image size 640 · batch 16 · GPU.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask, Python 3.10+ |
| Inference | Ultralytics YOLOv9, OpenCV |
| Preprocessing | CLAHE, Sharpening (cv2) |
| Analytics | Pandas, Matplotlib |
| Frontend | HTML/CSS (custom templates) |

---

## Project Structure

```
Realtime-Defect-Detection/
├── app.py
├── models/
├── templates/
├── static/
└── utils/
    ├── preprocessing.py
    ├── logger.py
    └── stats.py
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Webcam

### Setup

```bash
git clone https://github.com/hxrsha05/Realtime-Defect-Detection.git
cd Realtime-Defect-Detection

pip install flask ultralytics opencv-python pandas matplotlib

python app.py
```

Go to `http://localhost:5000`.

Model weights are not included due to file size. Train using the provided configs or reach out directly.

---

## Notes

- Zoom mode sends the cropped region — not the full frame — to the model
- Preprocessing is scoped to the weld model only
- Detection stats reset per session; CSV persists across runs

---

## Author

**Sri Harshavardhan Palaniswamy J**

