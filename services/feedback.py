import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


def get_ai_feedback(student):
    try:

        prompt = f"""
You are an academic mentor.

Student Details:

Email: {student['Email']}
Total Marks: {student['Total Marks']}
Percentage: {student['Percentage']}
Percentile: {student['Percentile']}
Rank: {student['Rank']}
Grade: {student['Grade']}

Quiz Scores:
Quiz 1: {student.get('Quiz_1', 0)}
Quiz 2: {student.get('Quiz_2', 0)}
Quiz 3: {student.get('Quiz_3', 0)}

Generate:
1. Strengths
2. Areas of improvement
3. Motivation

Keep it under 120 words.
"""

        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 250
        }

        response = requests.post(
            MISTRAL_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI feedback unavailable: {str(e)}"
    
    