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

DEFAULT_CROPS = [
    ('rice', 'Rice Leaf Blast', '92.4%', 'Apply Tricyclazole fungicide and avoid excess nitrogen fertilizer.', 'https://www.amazon.in/s?k=Tricyclazole+fungicide'),
    ('tomato', 'Tomato Early Blight', '89.8%', 'Remove infected leaves and spray Mancozeb or Copper-based fungicide.', 'https://www.amazon.in/s?k=Mancozeb+fungicide'),
    ('potato', 'Potato Late Blight', '94.1%', 'Use Metalaxyl fungicide and ensure proper field drainage.', 'https://www.amazon.in/s?k=Metalaxyl+fungicide'),
    ('chilli', 'Chilli Leaf Curl', '88.5%', 'Control whiteflies using Neem oil or Imidacloprid spray.', 'https://www.amazon.in/s?k=Neem+oil+for+plants')
]

# Initialize Relational SQLite Database (2 Tables: crops & scans)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            disease TEXT NOT NULL,
            confidence TEXT NOT NULL,
            remedy TEXT NOT NULL,
            buy_link TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM crops')
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO crops (name, disease, confidence, remedy, buy_link) VALUES (?, ?, ?, ?, ?)',
            DEFAULT_CROPS
        )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_id INTEGER,
            crop TEXT NOT NULL,
            filename TEXT NOT NULL,
            disease TEXT NOT NULL,
            confidence TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            timestamp TEXT NOT NULL,
            FOREIGN KEY (crop_id) REFERENCES crops(id)
        )
    ''')

    try:
        cursor.execute("ALTER TABLE scans ADD COLUMN status TEXT DEFAULT 'Pending'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE scans ADD COLUMN crop_id INTEGER")
    except sqlite3.OperationalError:
        pass

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
        'service': 'PLANTORA Backend API',
        'database': 'SQLite connected (plantora.db)'
    }), 200

# Route 3: READ - Fetch All Supported Crops & Remedies
@app.route('/api/crops', methods=['GET'])
def get_crops():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, disease, confidence, remedy FROM crops')
    rows = cursor.fetchall()
    conn.close()

    crops_list = [
        {
            'id': r[0],
            'name': r[1].capitalize(),
            'disease': r[2],
            'confidence': r[3],
            'remedy': r[4]
        }
        for r in rows
    ]
    return jsonify({'status': 'success', 'total_crops': len(crops_list), 'crops': crops_list}), 200

# Route 4: CREATE - Predict & Insert Scan into DB
@app.route('/predict', methods=['POST'])
def predict():
    crop_name = request.form.get('crop', '').strip().lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, disease, confidence, remedy, buy_link FROM crops WHERE name = ?', (crop_name,))
    crop_row = cursor.fetchone()

    if not crop_row:
        conn.close()
        return jsonify({'error': 'Invalid or unsupported crop type.'}), 400

    if 'image' not in request.files:
        conn.close()
        return jsonify({'error': 'No image file uploaded.'}), 400

    file = request.files['image']
    if file.filename == '' or not is_valid_image(file.filename):
        conn.close()
        return jsonify({'error': 'Invalid format. Please upload a JPG or PNG image.'}), 400

    if not is_leaf_image(file.stream):
        conn.close()
        return jsonify({'error': 'Invalid image! Please upload a clear plant leaf photo.'}), 400

    crop_id, disease, confidence, remedy, buy_link = crop_row
    scan_time = datetime.now().strftime('%d-%m-%Y %I:%M %p')

    cursor.execute(
        'INSERT INTO scans (crop_id, crop, filename, disease, confidence, status, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (crop_id, crop_name.capitalize(), file.filename, disease, confidence, 'Pending', scan_time)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'crop': crop_name.capitalize(),
        'uploaded_file': file.filename,
        'prediction': disease,
        'confidence': confidence,
        'remedy': remedy,
        'buy_link': buy_link,
        'timestamp': scan_time
    }), 200

# Route 5: READ - Fetch Scan History
@app.route('/history', methods=['GET'])
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, crop, filename, disease, confidence, status, timestamp FROM scans ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()

    history_list = [
        {
            'id': row[0],
            'crop': row[1],
            'filename': row[2],
            'disease': row[3],
            'confidence': row[4],
            'status': row[5] or 'Pending',
            'timestamp': row[6]
        }
        for row in rows
    ]
    return jsonify({'status': 'success', 'total_scans': len(history_list), 'history': history_list}), 200

# Route 6: UPDATE - Mark a scan as Treated
@app.route('/history/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE scans SET status = 'Treated' WHERE id = ?", (scan_id,))
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({'error': 'Scan record not found.'}), 404
    return jsonify({'status': 'success', 'message': f'Scan #{scan_id} marked as Treated.'}), 200

# Route 7: DELETE - Remove a scan record
@app.route('/history/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scans WHERE id = ?', (scan_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({'error': 'Scan record not found.'}), 404
    return jsonify({'status': 'success', 'message': f'Scan #{scan_id} deleted.'}), 200

# Route 8: View Both Database Tables
@app.route('/db-tables', methods=['GET'])
def db_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, disease, confidence FROM crops')
    crops = [{'id': r[0], 'name': r[1], 'disease': r[2], 'confidence': r[3]} for r in cursor.fetchall()]
    cursor.execute('SELECT id, crop_id, crop, disease, status, timestamp FROM scans ORDER BY id DESC')
    scans = [{'id': r[0], 'crop_id': r[1], 'crop': r[2], 'disease': r[3], 'status': r[4] or 'Pending', 'timestamp': r[5]} for r in cursor.fetchall()]
    conn.close()
    return jsonify({'database': 'plantora.db', 'tables': {'crops': crops, 'scans': scans}}), 200

# Global JSON Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'code': 404, 'message': 'API endpoint not found.'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'status': 'error', 'code': 405, 'message': 'HTTP method not allowed on this endpoint.'}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5000)