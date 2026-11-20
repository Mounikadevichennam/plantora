from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Allowed image formats and supported crops
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SUPPORTED_CROPS = ['rice', 'tomato', 'potato', 'chilli']

# Sample remedy database for initial backend testing
REMEDY_DATA = {
    'rice': {
        'disease': 'Rice Leaf Blast',
        'confidence': '92.4%',
        'remedy': 'Apply Tricyclazole fungicide and avoid excess nitrogen fertilizer.'
    },
    'tomato': {
        'disease': 'Tomato Early Blight',
        'confidence': '89.8%',
        'remedy': 'Remove infected leaves and spray Mancozeb or Copper-based fungicide.'
    },
    'potato': {
        'disease': 'Potato Late Blight',
        'confidence': '94.1%',
        'remedy': 'Use Metalaxyl fungicide and ensure proper field drainage.'
    },
    'chilli': {
        'disease': 'Chilli Leaf Curl',
        'confidence': '88.5%',
        'remedy': 'Control whiteflies using Neem oil or Imidacloprid spray.'
    }
}

def is_valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route 1: Health Check / Home
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'project': 'PLANTORA Backend API',
        'supported_crops': SUPPORTED_CROPS,
        'endpoints': {
            'health_check': 'GET /',
            'predict_disease': 'POST /predict'
        }
    }), 200

# Route 2: Crop Disease Prediction & Validation
@app.route('/predict', methods=['POST'])
def predict():
    crop = request.form.get('crop', '').strip().lower()
    
    # Validate crop type
    if crop not in SUPPORTED_CROPS:
        return jsonify({
            'error': 'Invalid or missing crop type.',
            'supported_crops': SUPPORTED_CROPS
        }), 400

    # Validate image upload
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded.'}), 400

    file = request.files['image']
    if file.filename == '' or not is_valid_image(file.filename):
        return jsonify({'error': 'Invalid file format. Please upload a JPG or PNG image.'}), 400

    # Simulated AI prediction response (ready for AI model integration)
    result = REMEDY_DATA[crop]
    return jsonify({
        'status': 'success',
        'crop': crop.capitalize(),
        'uploaded_file': file.filename,
        'prediction': result['disease'],
        'confidence': result['confidence'],
        'remedy': result['remedy']
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)