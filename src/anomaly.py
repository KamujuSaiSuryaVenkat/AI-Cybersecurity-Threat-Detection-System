from sklearn.ensemble import IsolationForest
import joblib

def train_anomaly_model(X):
    model = IsolationForest(contamination=0.1)
    model.fit(X)

    joblib.dump(model, "models/anomaly_model.pkl")
    return model

def detect_anomaly(model, X):
    preds = model.predict(X)
    
    # -1 = anomaly, 1 = normal
    return ["ATTACK" if p == -1 else "NORMAL" for p in preds]