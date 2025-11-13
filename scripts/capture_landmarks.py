# scripts/capture_landmarks.py
import cv2, csv, os, time
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
DATA_FILE = "data/landmarks.csv"
os.makedirs("data", exist_ok=True)

def landmarks_to_list(landmarks):
    return np.array([[l.x, l.y, l.z] for l in landmarks]).flatten().tolist()

cap = cv2.VideoCapture(0)
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6) as hands, \
     open(DATA_FILE, mode='a', newline='') as f:

    writer = csv.writer(f)
    print("Instructions:")
    print(" - Enter label name in terminal (e.g., A or hello) and press Enter")
    print(" - In the camera window, press 'c' to capture a frame for that label.")
    print(" - Press 'q' to quit.")

    while True:
        label = input("Enter label (or 'q' to quit): ").strip()
        if label.lower() == 'q':
            break
        print(f"Recording frames for label '{label}'. Press 'c' to capture each sample.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera failure")
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img)
            display = frame.copy()

            if results.multi_hand_landmarks:
                for hm in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(display, hm, mp_hands.HAND_CONNECTIONS)

            cv2.putText(display, f"Label: {label} | Press 'c' to capture, 'n' for next label, 'q' to quit",
                        (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.imshow("Capture - Press 'c' to save", display)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                if results.multi_hand_landmarks:
                    lm = results.multi_hand_landmarks[0].landmark
                    row = landmarks_to_list(lm)
                    writer.writerow([label] + row)
                    print("Saved sample for", label)
                else:
                    print("No hand detected. Adjust position/lighting.")
            elif key == ord('n'):
                break
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit(0)

cap.release()
cv2.destroyAllWindows()
