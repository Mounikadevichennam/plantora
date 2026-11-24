from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
DB_PATH = os.path.join(BASE_DIR, 'plantora.db')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SUPPORTED_CROPS = ['rice', 'tomato', 'potato', 'chilli']

REMEDY_DATA = {
    'rice': {
        'disease': 'Rice Leaf Blast',
        'confidence': '92.4%',
        'remedy': 'Apply Tricyclazole fungicide and avoid excess nitrogen fertilizer.',
        'buy_link': 'https://www.amazon.in/s?k=Tricyclazole+fungicide'
    },
    'tomato': {
        'disease': 'Tomato Early Blight',
        'confidence': '89.8%',
        'remedy': 'Remove infected leaves and spray Mancozeb or Copper-based fungicide.',
        'buy_link': 'https://www.amazon.in/s?k=Mancozeb+fungicide'
    },
    'potato': {
        'disease': 'Potato Late Blight',
        'confidence': '94.1%',
        'remedy': 'Use Metalaxyl fungicide and ensure proper field drainage.',
        'buy_link': 'https://www.amazon.in/s?k=Metalaxyl+fungicide'
    },
    'chilli': {
        'disease': 'Chilli Leaf Curl',
        'confidence': '88.5%',
        'remedy': 'Control whiteflies using Neem oil or Imidacloprid spray.',
        'buy_link': 'https://www.amazon.in/s?k=Neem+oil+for+plants'
    }
}

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT NOT NULL,
            filename TEXT NOT NULL,
            disease TEXT NOT NULL,
            confidence TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def is_valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_leaf_image(file_stream):
    try:
        img = Image.open(file_stream).convert('RGB')
        img = img.resize((100, 100))
        pixels = list(img.getdata())
        green_pixels = sum(1 for r, g, b in pixels if g > r and g > b and g > 40)
        return (green_pixels / len(pixels)) >= 0.12
    except Exception:
        return False

# Route 1: Serve Frontend UI
@app.route('/', methods=['GET'])
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Route 2: API Health Check
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'project': 'PLANTORA Backend API',
        'supported_crops': SUPPORTED_CROPS
    }), 200

# Route 3: Crop Disease Prediction & Save to DB
@app.route('/predict', methods=['POST'])
def predict():
    crop = request.form.get('crop', '').strip().lower()
    
    if crop not in SUPPORTED_CROPS:
        return jsonify({'error': 'Invalid or missing crop type.'}), 400

    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded.'}), 400

    file = request.files['image']
    if file.filename == '' or not is_valid_image(file.filename):
        return jsonify({'error': 'Invalid format. Please upload a JPG or PNG image.'}), 400

    if not is_leaf_image(file.stream):
        return jsonify({
            'error': 'Invalid image! This does not look like a crop leaf. Please upload a clear plant leaf photo.'
        }), 400

    result = REMEDY_DATA[crop]
    scan_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')

    # Save scan result to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO scans (crop, filename, disease, confidence, timestamp) VALUES (?, ?, ?, ?, ?)',
        (crop.capitalize(), file.filename, result['disease'], result['confidence'], scan_time)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'crop': crop.capitalize(),
        'uploaded_file': file.filename,
        'prediction': result['disease'],
        'confidence': result['confidence'],
        'remedy': result['remedy'],
        'buy_link': result['buy_link'],
        'timestamp': scan_time
    }), 200

# Route 4: Fetch Recent Scan History
@app.route('/history', methods=['GET'])
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT crop, filename, disease, confidence, timestamp FROM scans ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()

    history_list = [
        {
            'crop': row[0],
            'filename': row[1],
            'disease': row[2],
            'confidence': row[3],
            'timestamp': row[4]
        }
        for row in rows
    ]
    return jsonify({'status': 'success', 'total_scans': len(history_list), 'history': history_list}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)