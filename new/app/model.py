from ultralytics import YOLO

paint_model = YOLO("models/paint.pt")
weld_model = YOLO("models/weld.pt")
surface_model = YOLO("models/surface.pt")

def run_paint_model(frame, return_results=False):
    results = paint_model.predict(frame, conf=0.4, save=False, verbose=False)
    if return_results:
        return results

    boxes = results[0].boxes
    if len(boxes) == 0:
        return {
            'pass_fail': 'Pass',
            'defect': 'No paint defect',
            'reason': 'Paint surface appears clean',
            'can_reuse': 'Yes'
        }
    label = results[0].names[int(boxes.cls[0])]
    return {
        'pass_fail': 'Fail',
        'defect': label,
        'reason': 'Detected paint defect',
        'can_reuse': 'No'
    }

def run_weld_model(frame, return_results=False):
    results = weld_model.predict(frame, conf=0.4, save=False, verbose=False)
    if return_results:
        return results

    boxes = results[0].boxes
    if len(boxes) == 0:
        return {
            'pass_fail': 'Pass',
            'defect': 'No weld defect',
            'reason': 'Weld appears consistent',
            'can_reuse': 'Yes'
        }
    label = results[0].names[int(boxes.cls[0])]
    return {
        'pass_fail': 'Fail',
        'defect': label,
        'reason': 'Detected welding anomaly',
        'can_reuse': 'No'
    }

def run_surface_model(frame, return_results=False):
    results = surface_model.predict(frame, conf=0.4, save=False, verbose=False)
    if return_results:
        return results

    boxes = results[0].boxes
    if len(boxes) == 0:
        return {
            'pass_fail': 'Pass',
            'defect': 'No surface defect',
            'reason': 'Surface looks smooth',
            'can_reuse': 'Yes'
        }
    label = results[0].names[int(boxes.cls[0])]
    return {
        'pass_fail': 'Fail',
        'defect': label,
        'reason': 'Detected surface flaw',
        'can_reuse': 'No'
    }
