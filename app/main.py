from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="FitBuddy",
    description="AI Fitness Plan Generator using Gemini"
)

app.include_router(router)
