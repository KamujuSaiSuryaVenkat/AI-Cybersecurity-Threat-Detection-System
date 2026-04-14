from src.preprocessing import load_data, preprocess_data
from src.train_model import train_model
import joblib
from src.anomaly import train_anomaly_model, detect_anomaly


# Load dataset
data = load_data("data/dataset.csv")

# Preprocess
X, y, scaler = preprocess_data(data)

# Train
model = train_model(X, y)

# Save the scaler so the API can use it
joblib.dump(scaler, "models/scaler.pkl")

# Train anomaly model
anomaly_model = train_anomaly_model(X)

# Detect anomalies
results = detect_anomaly(anomaly_model, X[:10])

print(results)