from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from CurrentTransit import get_current_transit
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GemstoneRequest(BaseModel):
    cp: str

# Planet-gemstone mapping with astrological properties
planet_gemstone_map = {
    "Sun": {
        "gemstone": "Ruby",
        "properties": "Leadership, authority, confidence"
    },
    "Moon": {
        "gemstone": "Pearl",
        "properties": "Emotional balance, peace of mind, intuition"
    },
    "Mars": {
        "gemstone": "Red Coral", 
        "properties": "Energy, courage, ambition"
    },
    "Mercury": {
        "gemstone": "Emerald",
        "properties": "Intelligence, communication, business"
    }, 
    "Jupiter": {
        "gemstone": "Yellow Sapphire",
        "properties": "Wisdom, prosperity, spirituality"
    },
    "Venus": {
        "gemstone": "Diamond",
        "properties": "Love, relationships, arts"
    },
    "Saturn": {
        "gemstone": "Blue Sapphire", 
        "properties": "Discipline, responsibility, career"
    },
    "Rahu": {
        "gemstone": "Hessonite Garnet",
        "properties": "Material gains, overcoming obstacles"
    },
    "Ketu": {
        "gemstone": "Cat's Eye",
        "properties": "Spiritual growth, psychic abilities"
    }
}

@app.post("/gemstones/")
async def get_gemstone_recommendations(request: GemstoneRequest):
    # Get current transit data
    transit_data = json.loads(get_current_transit(request.cp))
    
    # Create output dictionary
    output = {
        "location": transit_data["location"],
        "timestamp": transit_data["timestamp"],
        "recommendations": [],
        "important_notes": [
            "Consult an experienced astrologer before wearing any gemstone",
            "Gemstones should be natural and of high quality", 
            "Best worn after proper energization and during auspicious times",
            "Consider your birth chart's complete analysis for optimal results"
        ]
    }

    # Add recommendations based on planetary positions
    for position in transit_data["positions"]:
        if "planet" in position:
            planet = position["planet"]
            if planet in planet_gemstone_map:
                recommendation = {
                    "planet": planet,
                    "position": {
                        "house": position["house"],
                        "rashi": position["rashi"]
                    },
                    "gemstone": planet_gemstone_map[planet]["gemstone"],
                    "benefits": planet_gemstone_map[planet]["properties"]
                }
                output["recommendations"].append(recommendation)

    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
