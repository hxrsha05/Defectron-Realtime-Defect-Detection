# Realtime Defect Detection

A Flask-based defect detection system that runs inference on a live camera feed using YOLOv9. Built to support industrial inspection use cases — surface, weld, and paint defects — with preprocessing, logging, and a stats dashboard.

---

## What it does

- Streams live camera feed and runs per-frame inference using YOLOv9
- Supports three separate models: surface, weld, paint
- Zoom mode crops the frame before passing it to the model — useful for catching fine-grained defects at a distance
- CLAHE + sharpening preprocessing applied selectively to the weld pipeline (metallic surfaces respond well; the other models don't need it)
- Logs every detection to a CSV with timestamps and class labels
- Displays running bar and pie charts broken down by defect class
- Segmentation masks overlaid on the live feed

---

## Models

| Target | Architecture | Training Data |
|--------|-------------|---------------|
| Surface | YOLOv9c | NEU-DET (6 classes) |
| Weld | YOLOv9c | Custom dataset |
| Paint | YOLOv9c | Custom dataset |

NEU-DET classes: `crazing`, `inclusion`, `patches`, `pitted_surface`, `rolled-in_scale`, `scratches`

Surface model trained at 100 epochs, image size 640, batch 16 on GPU.

---

## Setup

```bash
pip install flask ultralytics opencv-python pandas matplotlib
python app.py
```

Go to `http://localhost:5000`.

Model weights are not included due to file size. Train using the configs provided or reach out directly.

---

## Project structure

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

## Notes

- Zoom mode sends the cropped region, not the full frame, to the model
- Preprocessing is scoped to the weld model only — applying it elsewhere degrades accuracy
- Detection stats reset per session; CSV persists across runs

---

## Author

Sri Harshavardhan — AI/CS Engineering, PSG iTech  
[github.com/hxrsha05](https://github.com/hxrsha05)
