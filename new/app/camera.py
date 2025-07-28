from app.frame_manager import get_frame
from ultralytics import YOLO
import cv2
import os
import csv
from datetime import datetime

paint_model = YOLO("models/paint.pt")
weld_model = YOLO("models/weld.pt")
surface_model = YOLO("models/surface.pt")

def write_log(model_name, labels):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_filename = f'detections_{model_name}.csv'
    csv_path = os.path.join('logs', csv_filename)
    os.makedirs('logs', exist_ok=True)

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Pass/Fail', 'Defect Labels'])

        writer.writerow([timestamp, 'Fail', ", ".join(labels)])

def gen_frames(model='surface'):
    while True:
        frame = get_frame()
        if frame is None:
            continue

        if model == 'surface':
            results = surface_model(frame, verbose=False)
        elif model == 'paint':
            results = paint_model(frame, verbose=False)
        else:
            results = weld_model(frame, verbose=False)

        boxes = results[0].boxes
        if boxes and len(boxes.cls) > 0:
            labels = [results[0].names[int(cls)] for cls in boxes.cls]
            write_log(model, labels)

        output = results[0].plot()

        _, buffer = cv2.imencode('.jpg', output)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
