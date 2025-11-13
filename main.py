import cv2
import mediapipe as mp
import numpy as np
import joblib
import pyttsx3
from utils.preprocess import SignProcessor  # ✅ using your existing file
from utils.translator import grammar_fix  # ✅ Import grammar fix

# Load trained model
model = joblib.load("model/sign_model.pkl")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def lm_to_vector(landmarks):
    return np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()

cap = cv2.VideoCapture(0)

processor = SignProcessor(buffer_size=30)   # Further increased buffer size for better stability and accuracy

# Initialize TTS engine once outside the loop
engine = pyttsx3.init()

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        predicted_label = "No Hand"

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

                vector = lm_to_vector(hand_lms.landmark).reshape(1, -1)
                predicted_label = model.predict(vector)[0]

                # Update sentence via stable prediction
                stable_pred, sentence = processor.update(predicted_label)

                # Clear if STOP detected
                if stable_pred == "STOP":
                    processor.clear_sentence()
                    sentence = ""

        else:
            sentence = " ".join(processor.sentence)

        # Apply grammar fix to the sentence
        corrected_sentence = grammar_fix(sentence)

        # UI Text (Black Color)
        cv2.putText(img, f"Prediction: {predicted_label}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        cv2.putText(img, f"Sentence: {corrected_sentence}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        cv2.putText(img, "Press 'r' to Clear | 's' to Speak | 'e' to Export | ESC to Exit", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

        cv2.imshow("Sign Language Translator", img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('r'):  # Clear manually
            processor.clear_sentence()
        elif key == ord('s'):  # Speak the sentence
            if corrected_sentence.strip():
                engine.say(corrected_sentence)
                engine.runAndWait()
        elif key == ord('e'):  # Export sentence to file
            processor.export_sentence()

cap.release()
cv2.destroyAllWindows()
