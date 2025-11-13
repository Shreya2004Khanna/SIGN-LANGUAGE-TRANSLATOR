import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
import os

# Load data
DATA_FILE = "data/landmarks.csv"
data = pd.read_csv(DATA_FILE, header=None)

# First column is label
labels = data.iloc[:, 0]
# Remaining columns are features (landmarks)
features = data.iloc[:, 1:]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Create Model with more neighbors for better accuracy
model = KNeighborsClassifier(n_neighbors=7)
model.fit(X_train, y_train)

# Evaluate with cross-validation for robustness
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, features, labels, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean() * 100:.2f}%")

# Evaluate on test set
accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy * 100:.2f}%")

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/sign_model.pkl")
print("Model saved → model/sign_model.pkl")
