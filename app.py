import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
import base64
from preprocessing import preprocess_image
from fft_logic import apply_fft_filter
import io

app = Flask(__name__)

def encode_image(img, ext='.jpg', quality=88):
    """Helper to convert OpenCV image to a compact base64 data URL."""
    if img is None:
        return None

    params = []
    mime = 'image/png'
    if ext in ('.jpg', '.jpeg'):
        mime = 'image/jpeg'
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]

    _, buffer = cv2.imencode(ext, img, params)
    return f"data:{mime};base64,{base64.b64encode(buffer).decode('utf-8')}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Read image
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image format'}), 400

        # Process image
        preprocessed = preprocess_image(img)
        components = apply_fft_filter(preprocessed)

        # Unpack components
        orig, spectrum, mask, result, metrics = components

        return jsonify({
            'original': encode_image(orig),
            'spectrum': encode_image(spectrum),
            'filter': encode_image(mask),
            'result': encode_image(result),
            'metrics': metrics
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
