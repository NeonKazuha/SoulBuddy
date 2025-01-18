import json
from BirthTransit import birthtransit
from CurrentTransit import curtransit
import swisseph as swe
from datetime import datetime

def get_nakshatra(degree):
    # Each nakshatra spans 13°20' (13.3333... degrees)
    nakshatra_span = 13 + (1/3)
    nakshatra_index = int(degree / nakshatra_span)
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_index]

def calculate_dasha(moon_degree, birth_date):
    # Calculate Vimshottari dasha
    # Moon's nakshatra position determines the main dasha period
    nakshatra_span = 13 + (1/3)
    nakshatra_balance = (moon_degree % nakshatra_span) / nakshatra_span
    
    dasha_periods = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
        "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
    }
    
    dasha_order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    
    # Find starting dasha based on moon's nakshatra
    start_dasha_index = int(moon_degree / nakshatra_span) % 9
    current_dasha = dasha_order[start_dasha_index]
    
    return current_dasha

def get_prediction_for_aspect(planet, aspect_type):
    predictions = {
        'conjunction': {
            'Sun': 'A day of heightened self-awareness and vitality. Good for starting new projects.',
            'Moon': 'Emotional intensity and sensitivity. Pay attention to your intuition.',
            'Mercury': 'Enhanced communication and mental clarity. Favorable for important conversations.',
            'Venus': 'Increased charm and creativity. Excellent for relationships and artistic pursuits.',
            'Mars': 'High energy and motivation. Channel this energy into productive activities.',
            'Jupiter': 'Opportunities for growth and expansion. Lucky day for new ventures.',
            'Saturn': 'Important lessons and responsibilities. Focus on long-term goals.',
            'Uranus': 'Unexpected changes and innovations. Stay flexible and open to new ideas.',
            'Neptune': 'Heightened intuition and creativity. Good for spiritual practices.',
            'Pluto': 'Powerful transformations. Time for deep personal growth.'
        },
        'opposition': {
            'Sun': 'Potential conflicts with authority figures. Stay balanced and diplomatic.',
            'Moon': 'Emotional tensions may arise. Practice self-care and patience.',
            'Mercury': 'Communication challenges. Double-check important messages.',
            'Venus': 'Relationship dynamics may be strained. Focus on compromise.',
            'Mars': 'Energy might feel scattered. Avoid confrontations.',
            'Jupiter': 'Watch for overconfidence or excess. Practice moderation.',
            'Saturn': 'Obstacles may appear. Stay persistent but flexible.',
            'Uranus': 'Resist impulsive changes. Find balance between old and new.',
            'Neptune': 'Reality vs. illusion. Stay grounded and practical.',
            'Pluto': 'Power struggles possible. Transform challenges into growth.'
        }
    }
    return predictions.get(aspect_type, {}).get(planet, '')

def analyze_horoscope(birth_data, transit_data):
    aspects = []
    predictions = []
    nakshatras = []
    dashas = []
    daily_predictions = []

    # Get birth date from birth_data
    birth_timestamp = datetime.strptime(birth_data['timestamp'], '%Y-%m-%d %H:%M')

    # Step 1: Parse Data and Calculate Nakshatras
    for planet in birth_data['positions']:
        if 'planet' not in planet:
            continue
            
        birth_deg = planet["degree"]
        transit_planet = next(
            (p for p in transit_data['positions'] if 'planet' in p and p["planet"] == planet["planet"]),
            None
        )
        
        if not transit_planet:
            continue
            
        transit_deg = transit_planet["degree"]
        transit_house = transit_planet["house"] 
        transit_rashi = transit_planet["rashi"]
        
        # Calculate nakshatra for each planet
        birth_nakshatra = get_nakshatra(birth_deg)
        transit_nakshatra = get_nakshatra(transit_deg)
        nakshatras.append(f"{planet['planet']} birth nakshatra: {birth_nakshatra}, transit nakshatra: {transit_nakshatra}")
        
        # Calculate dasha if it's Moon
        if planet['planet'] == 'Moon':
            current_dasha = calculate_dasha(birth_deg, birth_timestamp)
            dashas.append(f"Current main dasha period: {current_dasha}")
        
        # Step 2: Calculate Aspects and Their Predictions
        degree_diff = abs(birth_deg - transit_deg)
        degree_diff = degree_diff % 360  # Normalize to 0-360°

        if abs(degree_diff - 0) <= 5:
            aspects.append(f"{planet['planet']} is in conjunction with its transit position")
            prediction = get_prediction_for_aspect(planet['planet'], 'conjunction')
            if prediction:
                daily_predictions.append(prediction)
        elif abs(degree_diff - 180) <= 5:
            aspects.append(f"{planet['planet']} is in opposition to its transit position")
            prediction = get_prediction_for_aspect(planet['planet'], 'opposition')
            if prediction:
                daily_predictions.append(prediction)
        elif abs(degree_diff - 120) <= 5:
            aspects.append(f"{planet['planet']} is in trine with its transit position")
        elif abs(degree_diff - 90) <= 5:
            aspects.append(f"{planet['planet']} is in square with its transit position")
        elif abs(degree_diff - 60) <= 5:
            aspects.append(f"{planet['planet']} is in sextile with its transit position")

        # Step 3: House and Rashi Analysis with Nakshatra influence
        if planet["house"] != transit_house:
            house_change = f"{planet['planet']} has moved from {planet['house']}th house to {transit_house}th house in {transit_rashi}"
            predictions.append(house_change)
        else:
            house_same = f"{planet['planet']} remains in the {transit_house}th house in {transit_rashi}"
            predictions.append(house_same)

    return {
        "aspects": aspects,
        "predictions": predictions,
        "nakshatras": nakshatras,
        "dashas": dashas,
        "daily_predictions": daily_predictions
    }

def generate_horoscope(birth_chart_json, current_transit_json):
    # Parse JSON strings into Python dictionaries
    birth_data = json.loads(birth_chart_json)
    transit_data = json.loads(current_transit_json)
    
    # Analyze the charts
    analysis = analyze_horoscope(birth_data, transit_data)
    
    # Format output
    horoscope = "Daily Horoscope Analysis:\n\n"
    
    horoscope += "Today's Predictions:\n"
    for prediction in analysis["daily_predictions"]:
        horoscope += f"- {prediction}\n"
        
    horoscope += "\nNakshatras:\n"
    for nakshatra in analysis["nakshatras"]:
        horoscope += f"- {nakshatra}\n"
        
    horoscope += "\nDasha Periods:\n"
    for dasha in analysis["dashas"]:
        horoscope += f"- {dasha}\n"
    
    horoscope += "\nPlanetary Aspects:\n"
    for aspect in analysis["aspects"]:
        horoscope += f"- {aspect}\n"
    
    horoscope += "\nPlanetary Movements:\n"
    for prediction in analysis["predictions"]:
        horoscope += f"- {prediction}\n"
        
    return horoscope

# Call generate_horoscope with birth transit and current transit data
horoscope = generate_horoscope(birthtransit, curtransit)
print(horoscope)
print(f"\nPredictions for aspects:\n{get_prediction_for_aspect('Sun', 'conjunction')}")
