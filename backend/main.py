from flask import Flask, request, jsonify
from recognition.gesture_recognizer import GestureRecognizer
import base64
import numpy as np
import cv2

app = Flask(__name__)
recognizer = GestureRecognizer()

@app.route('/recognize', methods=['POST'])
def recognize_gesture():
    """
    Endpoint to recognize a gesture from a base64 encoded image.
    """
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data found'}), 400

    # Decode the base64 image
    try:
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({'error': f'Error decoding image: {str(e)}'}), 400

    if img is None:
        return jsonify({'error': 'Could not decode image'}), 400

    # Recognize the gesture
    gesture, _ = recognizer.recognize(img)

    # Return the result
    gesture_data = {
        'gesture': gesture,
        'confidence': 0.99  # Placeholder confidence
    }
    
    return jsonify(gesture_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

