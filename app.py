from flask import Flask, request, render_template, redirect, jsonify
from xml.etree import ElementTree as ET
import os
import subprocess
import time
import uuid
import json
import re
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'results.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['robot_file']
        username = request.form.get('username', 'Anonymous')

        if not file or not file.filename.endswith('.robot'):
            return 'Invalid file format. Only .robot files allowed.', 400

        filename = f"{uuid.uuid4()}.robot"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # ✅ Create output and log paths
        basename = os.path.splitext(filename)[0]
        output_xml = os.path.join(UPLOAD_FOLDER, f"{basename}-output.xml")
        log_html = os.path.join(UPLOAD_FOLDER, f"{basename}-log.html")

        # 🛠 Run Robot Framework
        result = subprocess.run([
            'robot',
            '--output', output_xml,
            '--log', log_html,
            '--report', 'NONE',
            filepath
        ], capture_output=True, text=True)

        exec_time = -1  # fallback

        # ✅ Parse output.xml and calculate elapsed time
        if result.returncode == 0 and os.path.exists(output_xml):
            try:
                root = ET.parse(output_xml).getroot()
                status = root.find(".//suite/status")
                if status is not None:
                    # First try direct "elapsed"
                    if "elapsed" in status.attrib:
                        exec_time = round(float(status.attrib["elapsed"]), 2)
                        print(f"✅ Execution time parsed from <status>: {exec_time}s")
                    else:
                        start = status.attrib.get("starttime")
                        end = status.attrib.get("endtime")
                        if start and end:
                            start_dt = datetime.strptime(start, "%Y%m%d %H:%M:%S.%f")
                            end_dt = datetime.strptime(end, "%Y%m%d %H:%M:%S.%f")
                            delta = (end_dt - start_dt).total_seconds()
                            exec_time = round(delta, 2)
                            print(f"✅ Execution time calculated from timestamps: {exec_time}s")
                        else:
                            print("⚠️ No start/end time found.")
                else:
                    print("⚠️ <status> tag not found.")
            except Exception as e:
                print("⚠️ XML parse error:", e)
        else:
            print("⚠️ Robot execution failed or output.xml missing.")

        # ✨ LOG RESULT TO JSON FILE
        log_result(username, exec_time)

        return redirect('/leaderboard')

    return render_template('upload.html')

@app.route('/leaderboard')
def leaderboard():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, encoding='utf-8-sig') as f:
        data = json.load(f)

    sorted_data = sorted(data, key=lambda x: x['duration'])
    return render_template('leaderboard.html', data=sorted_data)

def log_result(name, duration):
    entry = {
        "name": name,
        "duration": duration,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding='utf-8-sig') as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/api/results')
def api_results():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, encoding='utf-8-sig') as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
