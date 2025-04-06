from fastapi import FastAPI
from app.predict import predict_router

app = FastAPI()
app.include_router(predict_router)
