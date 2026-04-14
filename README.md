# 🔍 Realtime Defect Detection

A real-time industrial defect detection system built with Flask and YOLOv9, supporting live camera inference across multiple defect domains — with preprocessing, logging, and visual analytics.

---

## ✨ Features

- **Live Camera Inference** — Real-time detection streamed directly from a webcam feed
- **Multi-Model Support** — Switch between specialized models for:
  - Surface defects (NEU-DET dataset)
  - Weld defects
  - Paint defects
- **Zoom Mode** — Crops and passes a zoomed region to the model for closer inspection
- **CLAHE + Sharpening Preprocessing** — Applied selectively to the weld model pipeline for improved contrast on metallic surfaces
- **Segmentation Visualization** — Overlays segmentation masks on detected regions
- **CSV Logging** — Automatically logs all detections with timestamps and labels
- **Label-wise Statistics** — Live bar and pie charts showing detection distribution per class
- **Custom HTML UI** — Clean, purpose-built frontend templates

---

## 🧠 Model Details

| Model | Dataset | Architecture | Classes |
|-------|---------|--------------|---------|
| Surface | NEU-DET | YOLOv9c | crazing, inclusion, patches, pitted\_surface, rolled-in\_scale, scratches |
| Weld | Custom | YOLOv9c | — |
| Paint | Custom | YOLOv9c | — |

Surface model trained at: `100 epochs · image size 640 · batch 16 · GPU`

---

## 🗂️ Project Structure

```
Realtime-Defect-Detection/
├── app.py                  # Flask app entry point
├── models/                 # YOLOv9 model weights
├── templates/              # HTML UI templates
├── static/                 # CSS, JS, assets
├── utils/
│   ├── preprocessing.py    # CLAHE + sharpening pipeline
│   ├── logger.py           # CSV detection logger
│   └── stats.py            # Chart generation utilities
└── runs/                   # Inference outputs
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install flask ultralytics opencv-python pandas matplotlib
```

### Run

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## 📊 Analytics

Detections are logged in real time to a `.csv` file. The dashboard displays:
- **Bar chart** — count per defect class
- **Pie chart** — distribution of defect types across the session

---

## 📌 Notes

- CLAHE preprocessing is scoped only to the **weld model** to avoid degrading performance on other model types
- Zoom mode passes the cropped frame (not the full feed) to the model for inference
- Model weights are not included in this repo due to size — train using the provided configs or contact for access

---

## 🧑‍💻 Author

**Sri Harshavardhan Palaniswamy J** 
