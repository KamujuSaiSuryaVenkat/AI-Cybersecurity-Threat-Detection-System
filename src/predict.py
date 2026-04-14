import joblib

def load_model():
    return joblib.load("models/model.pkl")

def predict(model, sample):
    return model.predict(sample)