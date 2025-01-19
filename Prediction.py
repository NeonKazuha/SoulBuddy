import json
from groq import Groq
import os
from dotenv import load_dotenv
from FindHoroscope import generate_horoscope, get_horoscope

load_dotenv()

def generate_predictions(dob: str, tob: str, pob: str, cp: str):
    horoscope_data = get_horoscope(dob, tob, pob, cp)
    
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""Based on the following astrological data, generate detailed predictions and advice:

{horoscope_data}

Please provide:
1. Overall theme for the day
2. Career and professional insights
3. Relationship guidance
4. Health and wellbeing recommendations
5. Personal growth opportunities
6. Do's and Dont's for today
7. Give Workouts and Meditations based on horoscope
8. sleep content based on the persons horoscope
9. Lucky colour and Lucky Charm

Format the response in clear sections."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="mixtral-8x7b-32768", 
        temperature=0.7,
    )

    predictions = chat_completion.choices[0].message.content

    return predictions

def format_predictions(predictions):
    """Format the predictions in a clean, readable way"""
    formatted = "🌟 AI-Enhanced Astrological Predictions 🌟\n\n"
    formatted += predictions
    return formatted

def get_predictions(dob: str, tob: str, pob: str, cp: str):
    try:
        predictions = generate_predictions(dob, tob, pob, cp)
        formatted_predictions = format_predictions(predictions)
        return {"predictions": formatted_predictions}
    except Exception as e:
        return {"error": str(e)}
