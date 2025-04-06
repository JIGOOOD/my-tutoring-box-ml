from fastapi import APIRouter
from app.schemas import StudentInput
import numpy as np
import joblib

predict_router = APIRouter()

labels = {
    0: "개념 부족형",
    1: "준킬러 취약형",
    2: "킬러 취약형",
    3: "전략 부족형",
    4: "전반적 우수형"
}

model = joblib.load("model/student_type_classifier_100k.pkl")

@predict_router.post("/predict")
def predict(input_data: StudentInput):
    X = np.array([input_data.answers])
    prediction = model.predict(X)[0]
    return {
        "label": int(prediction),
        "type": labels[int(prediction)]
    }
