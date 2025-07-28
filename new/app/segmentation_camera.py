from app.frame_manager import get_frame
from ultralytics import YOLO
import cv2

segment_model = YOLO("models/weld_segment.pt")

def gen_segmented_frames(model='weld'):
    while True:
        frame = get_frame()
        if frame is None:
            continue

        results = segment_model(frame, verbose=False)
        mask_frame = results[0].plot(labels=False, boxes=False)

        _, buffer = cv2.imencode('.jpg', mask_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
