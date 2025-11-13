from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the retrained model
model = tf.keras.models.load_model('my_model_updated.keras')

# Class labels
class_labels = [f"Person {i:05d}" for i in range(10)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Open image
        image = Image.open(io.BytesIO(file.read()))
        # Resize to 64x64
        image = image.resize((64, 64))
        # Convert to RGB if not
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Predict
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = float(predictions[0][predicted_class])

        result = {
            'person': class_labels[predicted_class],
            'confidence': confidence
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
