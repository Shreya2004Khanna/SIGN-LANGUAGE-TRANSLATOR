from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
import joblib
from utils.preprocess import SignProcessor
from utils.translator import grammar_fix
from threading import Lock

app = Flask(__name__)

# Load Model (saved with joblib)
try:
    model = joblib.load("model/sign_model.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model 'model/sign_model.pkl': {e}")

# Processor for building sentence
processor = SignProcessor(buffer_size=6)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Shared sentence state and lock for simple thread-safety
sentence_global = ""
sentence_lock = Lock()

def generate_frames():
    """Capture frames, draw landmarks, run prediction and yield multipart JPEG frames.

    Camera and MediaPipe Hands are opened inside the generator so they are
    released when the generator ends (client disconnect or server shutdown).
    """
    cap = cv2.VideoCapture(0)

    # Use context manager for MediaPipe Hands to ensure proper cleanup
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(img_rgb)

                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract landmarks for prediction
                    coords = []
                    for lm in result.multi_hand_landmarks[0].landmark:
                        coords.extend([lm.x, lm.y, lm.z])
                    coords = np.array(coords).reshape(1, -1)

                    try:
                        prediction = model.predict(coords)[0]
                    except Exception:
                        prediction = None

                    if prediction is not None:
                        stable_pred, sentence = processor.update(prediction)
                        # Update global sentence safely
                        with sentence_lock:
                            sentence_global_local = grammar_fix(sentence)
                            # assign to shared state
                            global sentence_global
                            sentence_global = sentence_global_local

                # Encode frame for streaming
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        finally:
            cap.release()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_sentence')
def get_sentence():
    # read shared sentence safely
    with sentence_lock:
        return jsonify({"sentence": sentence_global})


@app.route('/clear', methods=['POST'])
def clear_sentence():
    global sentence_global
    processor.clear_sentence()
    with sentence_lock:
        sentence_global = ""
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)
