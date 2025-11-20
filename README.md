Sign Language Translator

A simple project that captures hand gestures through a webcam and translates them into text using a machine learning model.

📌 Features

Real-time sign detection

Converts gestures to text

ML model trained using scikit-learn

Easy-to-use web interface (HTML + JS)

Flask backend for predictions

🛠️ Technology Stack

Python (Flask) – Backend

OpenCV – Image processing

scikit-learn – ML model

HTML, CSS, JavaScript – Frontend

📂 Project Structure
/model        → trained_model.pkl
/static       → script.js, styles.css
/templates    → index.html
app.py
README.md

▶ How to Run

Install dependencies

pip install -r requirements.txt


Start backend

python app.py
