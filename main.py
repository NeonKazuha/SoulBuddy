from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Prediction import get_predictions
from FindHoroscope import get_horoscope, generate_horoscope
from CurrentTransit import get_current_transit
from BirthTransit import get_birth_transit

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class HoroscopeRequest(BaseModel):
    dob: str  
    tob: str  
    pob: str  
    cp: str   

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
