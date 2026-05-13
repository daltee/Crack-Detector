import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
import base64
from preprocessing import preprocess_image
from fft_logic import apply_fft_filter
import io
from PIL import Image

app = Flask(__name__)

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
        result = apply_fft_filter(preprocessed)

        # Convert result back to image for response
        _, buffer = cv2.imencode('.png', result)
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'result': f'data:image/png;base64,{encoded_image}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
