import sys
import os
import datetime
import joblib
import numpy as np
from flask import Flask, request, jsonify

# Ensure system can find 'src' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.alert import generate_alert
from src.logger import log_event

app = Flask(__name__)

# -------------------------------
# LOAD MODEL + SCALER SAFELY
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"❌ Scaler not found at {SCALER_PATH}")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# -------------------------------
# ROOT ROUTE (FIX FOR 404)
# -------------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 AI Cybersecurity Threat Detection API is running",
        "endpoint": "/predict",
        "method": "POST"
    })

# -------------------------------
# HEALTH CHECK ROUTE
# -------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "OK"})

# -------------------------------
# PREDICTION API
# -------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        # -------------------------------
        # FEATURE EXTRACTION
        # -------------------------------
        raw_features = np.array([[ 
            float(data.get("duration", 0)),
            float(data.get("protocol_type", 1)),
            float(data.get("service", 1)),
            float(data.get("src_bytes", 0)),
            float(data.get("dst_bytes", 0)),
            float(data.get("count", 0)),
            float(data.get("srv_count", 0)),
            float(data.get("serror_rate", 0)),
            float(data.get("srv_serror_rate", 0)),
            float(data.get("same_srv_rate", 1))
        ]])

        # -------------------------------
        # MODEL PREDICTION
        # -------------------------------
        scaled_features = scaler.transform(raw_features)
        prediction = model.predict(scaled_features)[0]

        is_attack = int(prediction) == 1

        # -------------------------------
        # SECURITY INTELLIGENCE LOGIC
        # -------------------------------
        severity = "LOW"
        attack_type = "Normal Activity"
        reason = "Traffic behavior aligns with standard network baselines."

        if is_attack:
            if float(data.get("serror_rate", 0)) > 0.5:
                attack_type = "DoS Attack"
                severity = "HIGH"
                reason = "High SYN-error rate → possible DoS attack."

            elif float(data.get("count", 0)) > 250:
                attack_type = "Network Scan / Probe"
                severity = "MEDIUM"
                reason = "High connection count → possible scanning."

            else:
                attack_type = "Anomalous Intrusion"
                severity = "MEDIUM"
                reason = "Behavior deviates from normal patterns."

        # -------------------------------
        # RESPONSE
        # -------------------------------
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = {
            "result": "🚨 ATTACK" if is_attack else "✅ NORMAL",
            "prediction": int(prediction),
            "attack_type": attack_type,
            "severity": severity,
            "reason": reason,
            "timestamp": timestamp,
            "alert": generate_alert(int(prediction))
        }

        # Log event
        log_event(data, response["result"])

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Prediction failed"
        }), 400

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)