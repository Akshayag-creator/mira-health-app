import os
import httpx
import joblib
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = joblib.load("health_model.pkl")

def get_local_prediction(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    bmi_estimate = round(cholesterol / 5.2, 1)
    age_estimate = 35
    insulin_estimate = round(glucose * 1.2, 1)
    bp_estimate = round(haemoglobin * 5.0, 1)

    features = pd.DataFrame([[glucose, bmi_estimate, age_estimate, insulin_estimate, bp_estimate]],
            columns=["Glucose", "BMI", "Age", "Insulin", "BloodPressure"])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    risk_percent = round(probability * 100, 1)

    if prediction == 1:
        if risk_percent >= 75:
            level = "Very High"
            advice = (
                "Critically elevated values detected. Immediate medical consultation is strongly advised. "
                "High risk of diabetes or related complications."
            )
        else:
            level = "High"
            advice = (
                "Blood test values indicate elevated health risk. "
                "Recommend consulting a doctor for further evaluation and lifestyle changes."
            )
    else:
        if risk_percent <= 25:
            level = "Low"
            advice = (
                "Blood test values are within a healthy range. "
                "Maintain a balanced diet and regular exercise to stay healthy."
            )
        else:
            level = "Moderate"
            advice = (
                "Some values are slightly outside the optimal range. "
                "Monitor regularly and consider consulting a healthcare professional."
            )

    return f"Risk Level: {level} ({risk_percent}%). {advice}"

async def get_health_prediction(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    """Try Gemini API first, fall back to local ML model if quota exceeded or any error."""
    prompt = f"""You are a medical assistant AI. Based on the following blood test results, 
    provide a brief health risk assessment in 2-3 sentences. Be concise and factual.

    Blood Test Results:
    - Glucose: {glucose} mg/dL
    - Haemoglobin: {haemoglobin} g/dL
    - Cholesterol: {cholesterol} mg/dL

    Give a short health prediction or risk summary."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-latest:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body, timeout=20.0)
            result = response.json()

            if "error" in result:
                print(f"Gemini API error: {result['error'].get('status')} — using local ML model as fallback.")
                return get_local_prediction(glucose, haemoglobin, cholesterol)

            return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print(f"Gemini API exception: {e} — using local ML model as fallback.")
        return get_local_prediction(glucose, haemoglobin, cholesterol)
    
    