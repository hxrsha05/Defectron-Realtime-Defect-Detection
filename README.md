# 🔧 Real-Time Industrial Defect Detection System using YOLO 🚀

A real-time computer vision system designed to detect and segment weld, paint, and surface defects using powerful YOLOv8/9/10 architectures. Built to support **automated inspection** in industrial settings like manufacturing and assembly lines, this system achieves high-speed inference with high precision on edge GPUs.

---

## 📌 Project Overview

This project integrates **four specialized YOLO models** to detect and segment defects in real time:

| Defect Type      | Model Used       | Model Type    | Architecture Highlights           |
|------------------|------------------|---------------|-----------------------------------|
| Weld Defects     | `YOLOv10-m`      | Object Detection | Anchor-Free, RepVi, Unified Head |
| Paint Defects    | `YOLOv9-c`       | Object Detection | Lightweight & Fast, PAN-FPN      |
| Weld Segmentation| `YOLOv8-seg`     | Segmentation     | Fine Mask Prediction              |
| Surface Defects  | `YOLOv9-c`       | Object Detection | Optimized for Edge Inference     |

Each model is deployed with **GPU acceleration**, custom preprocessing (denoising, sharpening, CLAHE), and a **zoom feature** for closer inspection.

---

## 🖥️ Technologies Used

- **Python 3.10**
- **OpenCV**
- **Ultralytics YOLOv8 / YOLOv9 / YOLOv10**
- **Torch + CUDA (GPU Inference)**
- **Real-time Camera Feed**
- **Image Preprocessing (CLAHE, Median Blur, Sharpening)**

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash

