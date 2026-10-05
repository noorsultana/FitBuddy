from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FitBuddy - AI Fitness Plan Generator"}
