import os

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, User
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan


router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/generate-workout")
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    workout_plan = generate_workout_gemini(
        age, weight, goal, intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    db = SessionLocal()

    user = User(
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(user)
    db.commit()
    db.close()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        db.close()
        return {"error": "User not found"}

    updated_plan = update_workout_plan(
        user.original_plan,
        feedback
    )

    user.updated_plan = updated_plan

    db.commit()
    db.close()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated_plan,
            "nutrition_tip": user.nutrition_tip
        }
    )


@router.get("/view-all-users")
def view_all_users(request: Request):
    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users
        }
    )
