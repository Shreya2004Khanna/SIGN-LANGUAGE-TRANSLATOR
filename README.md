Sign Language Translator – README
Overview

A simple Sign Language Translator that uses a webcam to capture hand gestures and converts them into text using a trained machine learning model.

Features

Real-time hand gesture capture

ML model prediction (scikit-learn)

Converts signs to text

Simple Flask backend + HTML/JS frontend

Tech Stack

Python, Flask – Backend API

OpenCV – Image capture & preprocessing

scikit-learn – Gesture recognition model

HTML, CSS, JavaScript – Frontend UI

How to Run

Install requirements:

pip install -r requirements.txt


Start server:

python app.py


Open in browser:
http://127.0.0.1:5000

Project Structure
model/ (saved ML model)
static/ (JS + CSS)
templates/ (HTML)
app.py
