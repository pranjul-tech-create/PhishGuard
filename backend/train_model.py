import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import joblib


# Load processed dataset
df = pd.read_csv("../dataset/processed_dataset.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# Separate features and target
X = df.drop("label", axis=1)
y = df["label"]


# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# Train model
print("\nTraining model...")

model.fit(X_train, y_train)

print("Model training completed!")


# Make predictions
y_pred = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)


# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Save trained model
model_file = "../backend/phishing_model.pkl"

joblib.dump(model, model_file)

print("\nModel saved successfully!")
print("Saved to:", model_file)