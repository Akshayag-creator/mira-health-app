import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv("dataset/diabetes.csv")

features = ["Glucose", "BMI", "Age", "Insulin", "BloodPressure"]
X = df[features]
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {round(accuracy * 100, 2)}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

joblib.dump(model, "health_model.pkl")
print("\nModel saved as health_model.pkl")

