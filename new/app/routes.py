from flask import Flask, render_template, Response, request, jsonify
from app.camera import gen_frames
from app.segmentation_camera import gen_segmented_frames
from app.model import run_paint_model, run_weld_model, run_surface_model
from app.rag_chain import query_rag
from app.frame_manager import get_frame, set_zoom
import csv
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/analyze')
def analyze():
    model_name = request.args.get('model', default='surface')
    frame = get_frame()
    if frame is None:
        return "Failed to access camera", 500

    if model_name == 'surface':
        result = run_surface_model(frame)
    elif model_name == 'paint':
        result = run_paint_model(frame)
    elif model_name == 'weld':
        result = run_weld_model(frame)
    else:
        result = {'status': 'error', 'message': 'Invalid model type'}

    return render_template('analyze.html', result=result, model=model_name)

@app.route('/video_feed')
def video_feed():
    model = request.args.get('model', default='surface')
    return Response(gen_frames(model), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/segmentation_feed')
def segmentation_feed():
    model = request.args.get('model', default='weld')
    return Response(gen_segmented_frames(model), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run_model')
def run_model():
    model_name = request.args.get('model', 'weld')
    frame = get_frame()
    if frame is None:
        return jsonify({'error': 'Could not read from camera'}), 500

    if model_name == 'surface':
        result = run_surface_model(frame)
    elif model_name == 'paint':
        result = run_paint_model(frame)
    elif model_name == 'weld':
        result = run_weld_model(frame)
    else:
        return jsonify({'error': 'Invalid model name'}), 400

    explanation = query_rag(result['defect'])
    return jsonify({
        "label": result['defect'],
        "pass_fail": result['pass_fail'],
        "reason": explanation,
        "repair": result['can_reuse']
    })

@app.route('/run_detection', methods=['POST'])
def run_detection():
    data = request.get_json()
    model = data.get('model', 'surface')
    frame = get_frame()
    if frame is None:
        return jsonify({'error': 'Camera not accessible'}), 500

    if model == 'surface':
        result = run_surface_model(frame)
    elif model == 'paint':
        result = run_paint_model(frame)
    elif model == 'weld':
        result = run_weld_model(frame)
    else:
        result = {
            'pass_fail': 'Unknown',
            'defect': 'Unknown',
            'reason': 'Invalid model selected',
            'can_reuse': 'Unknown'
        }

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    defects = result['defect']

    if isinstance(defects, list):
        rows = [[timestamp, 'Fail', defect, result['reason'], result['can_reuse']] for defect in defects]
    else:
        rows = [[timestamp, result['pass_fail'], defects, result['reason'], result['can_reuse']]]

    csv_filename = f'detections_{model}.csv'
    csv_path = os.path.join('logs', csv_filename)
    os.makedirs('logs', exist_ok=True)
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Timestamp', 'Pass/Fail', 'Defect', 'Reason', 'Can Repair/Reuse'])
        writer.writerows(rows)

    return jsonify(result)

@app.route('/logs')
def view_logs():
    model = request.args.get('model', 'surface')
    csv_file = os.path.join('logs', f'detections_{model}.csv')

    entries = []
    stats = {
        "defects": Counter()
    }

    if os.path.exists(csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader, [])
            for row in reader:
                entries.append(row)
                # Count defect class names individually
                if row[2]:  # row[2] is defect
                    for defect in row[2].split(','):
                        stats["defects"][defect.strip()] += 1
    else:
        headers = ["Timestamp", "Pass/Fail", "Defect", "Reason", "Can Repair/Reuse"]

    return render_template(
        'logs.html',
        model=model.capitalize(),
        headers=headers,
        entries=entries,
        stats=stats
    )

@app.route('/zoom')
def zoom():
    try:
        delta = float(request.args.get('delta', 0))
        set_zoom(delta)
        return "Zoom updated", 200
    except Exception as e:
        return str(e), 400
