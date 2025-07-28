import cv2
import threading

cap = cv2.VideoCapture(1)
latest_frame = None
zoom_factor = 1.0

def apply_zoom(frame, zoom):
    if zoom <= 1.0:
        return frame
    h, w = frame.shape[:2]
    new_w, new_h = int(w / zoom), int(h / zoom)
    x1 = max((w - new_w) // 2, 0)
    y1 = max((h - new_h) // 2, 0)
    x2 = x1 + new_w
    y2 = y1 + new_h
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

def update():
    global latest_frame
    while True:
        success, frame = cap.read()
        if success:
            latest_frame = frame.copy()

t = threading.Thread(target=update, daemon=True)
t.start()

def get_frame():
    global latest_frame, zoom_factor
    if latest_frame is None:
        return None
    return apply_zoom(latest_frame, zoom_factor)

def set_zoom(delta):
    global zoom_factor
    zoom_factor = max(1.0, min(2.0, zoom_factor + delta))

def get_zoom():
    return zoom_factor
