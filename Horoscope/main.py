from fastapi import FastAPI
from pydantic import BaseModel
from Prediction import get_predictions
from FindHoroscope import get_horoscope, generate_horoscope
from CurrentTransit import get_current_transit
from BirthTransit import get_birth_transit

app = FastAPI()

# Define the request body structure
class HoroscopeRequest(BaseModel):
    dob: str  # Date of birth (YYYY-MM-DD)
    tob: str  # Time of birth (HH:MM)
    pob: str  # Place of birth
    cp: str   # Current place

@app.post("/horoscope/")
async def get_horoscope_data(request: HoroscopeRequest):
    # Get birth transit data
    birth_transit = get_birth_transit(
        dob=request.dob,
        tob=request.tob,
        pob=request.pob
    )
    
    # Get current transit data
    current_transit = get_current_transit(request.cp)
    
    # Get horoscope analysis
    horoscope = get_horoscope(
        dob=request.dob,
        tob=request.tob,
        pob=request.pob,
        cp=request.cp
    )
    
    # Get AI predictions
    predictions = get_predictions(
        dob=request.dob,
        tob=request.tob,
        pob=request.pob,
        cp=request.cp
    )
    
    return {
        "birth_transit": birth_transit,
        "current_transit": current_transit, 
        "horoscope_analysis": horoscope,
        "ai_predictions": predictions
    }
