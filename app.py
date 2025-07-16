from flask import Flask, request, render_template, redirect, jsonify
from xml.etree import ElementTree as ET
import os
import subprocess
import time
import uuid
import json

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

        output_xml = filepath.replace('.robot', '-output.xml')

        # 🔧 Run Robot Framework with XML output
        subprocess.run(['robot', '--output', output_xml, filepath], capture_output=True, text=True)

        # 🕒 Parse the XML for actual elapsed time
        try:
            tree = ET.parse(output_xml)
            root = tree.getroot()
            elapsed_ms = int(root.find(".//suite").attrib.get("elapsedtime", 0))
            exec_time = round(elapsed_ms / 1000, 2)
        except Exception as e:
            exec_time = -1  # fallback for error

        log_result(username, exec_time)

        return redirect('/leaderboard')

    return render_template('upload.html')


@app.route('/leaderboard')
def leaderboard():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE) as f:
        data = json.load(f)

    # 🥇 Sort leaderboard by execution time (ascending)
    sorted_data = sorted(data, key=lambda x: x['duration'])
    return render_template('leaderboard.html', data=sorted_data)

def log_result(name, duration):
    entry = {
        "name": name,
        "duration": duration,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/form')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api/results')
def api_results():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE) as f:
        data = json.load(f)

    return jsonify(data)