import json
from groq import Groq
import os
from dotenv import load_dotenv
from FindHoroscope import generate_horoscope, birthtransit, curtransit

load_dotenv()

def generate_predictions():
    horoscope_data = generate_horoscope(birthtransit, curtransit)
    
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

Format the response in clear sections."""

    # Call Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="mixtral-8x7b-32768",  # Using Mixtral model for comprehensive analysis
        temperature=0.7,
    )

    predictions = chat_completion.choices[0].message.content

    return predictions

def format_predictions(predictions):
    """Format the predictions in a clean, readable way"""
    formatted = "🌟 AI-Enhanced Astrological Predictions 🌟\n\n"
    formatted += predictions
    return formatted

if __name__ == "__main__":
    try:
        predictions = generate_predictions()
        formatted_predictions = format_predictions(predictions)
        print(formatted_predictions)
    except Exception as e:
        print(f"Error generating predictions: {str(e)}")
