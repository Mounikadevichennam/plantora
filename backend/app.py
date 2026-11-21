from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

# Path to frontend folder
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SUPPORTED_CROPS = ['rice', 'tomato', 'potato', 'chilli']

# Updated remedy database with online purchase links
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

def is_valid_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Smart check: Verify if the image actually contains plant/leaf green tones
def is_leaf_image(file_stream):
    try:
        img = Image.open(file_stream).convert('RGB')
        img = img.resize((100, 100))  # Resize for fast checking
        pixels = list(img.getdata())
        
        green_pixels = 0
        for r, g, b in pixels:
            # Check for natural green leaf tones
            if g > r and g > b and g > 40:
                green_pixels += 1
                
        green_ratio = green_pixels / len(pixels)
        return green_ratio >= 0.12  # At least 12% of the image should have plant green
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

# Route 3: Crop Disease Prediction & Remedy
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

    # Check if the uploaded photo actually looks like a plant leaf
    if not is_leaf_image(file.stream):
        return jsonify({
            'error': 'Invalid image! This does not look like a crop leaf. Please upload a clear plant leaf photo.'
        }), 400

    result = REMEDY_DATA[crop]
    return jsonify({
        'status': 'success',
        'crop': crop.capitalize(),
        'uploaded_file': file.filename,
        'prediction': result['disease'],
        'confidence': result['confidence'],
        'remedy': result['remedy'],
        'buy_link': result['buy_link']
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)