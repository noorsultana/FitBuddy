import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def update_workout_plan(original_plan, feedback):
    prompt = f"""
Here is the original workout plan:

{original_plan}

User feedback:
{feedback}

Create an updated version of the workout plan based on the feedback.
Keep it clear and general.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text
