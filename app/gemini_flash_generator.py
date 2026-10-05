import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_nutrition_tip_with_flash(goal):
    prompt = f"""
Give one short, general healthy nutrition or recovery tip
related to this fitness goal: {goal}.

Keep it simple and practical.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
