import joblib
import os

MODEL_PATH = os.path.join("model", "student_type_classifier_10k.pkl")

def load_model():
    return joblib.load(MODEL_PATH)
