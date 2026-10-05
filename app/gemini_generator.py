import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_workout_gemini(age, weight, goal, intensity):
    prompt = f"""
Create a general 7-day fitness plan.

Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

For each day include:
- Warm-up
- Main workout
- Cool-down or recovery

Keep the plan clear and easy to follow.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text
