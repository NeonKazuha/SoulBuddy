import swisseph as swe
from opencage.geocoder import OpenCageGeocode
import os
from dotenv import load_dotenv
import json

load_dotenv()
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

def calculate_sidereal_positions_with_houses(date, time, latitude, longitude):
    # Parse input date and time
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
    decimal_time = hour + (minute / 60.0)

    # Calculate Julian Day
    jd = swe.julday(year, month, day, decimal_time)

    # Set Lahiri Ayanamsa (Vedic astrology)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    indian_zodiac = [
        'Mesha (Aries)', 'Vrishabha (Taurus)', 'Mithuna (Gemini)', 'Karka (Cancer)',
        'Simha (Leo)', 'Kanya (Virgo)', 'Tula (Libra)', 'Vrischika (Scorpio)',
        'Dhanu (Sagittarius)', 'Makara (Capricorn)', 'Kumbha (Aquarius)', 'Meena (Pisces)'
    ]

    planets = {
        swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
        swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
        swe.SATURN: 'Saturn', swe.URANUS: 'Uranus', swe.NEPTUNE: 'Neptune',
        swe.PLUTO: 'Pluto'
    }

    # Calculate Ascendant (Lagna)
    houses_cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    ascendant = ascmc[0]  # Ascendant degree

    house_positions = list(houses_cusps)

    results = []

    for planet, planet_name in planets.items():
        # Calculate planetary position
        position, _ = swe.calc_ut(jd, planet)

        # Adjust for Ayanamsa (Sidereal calculation)
        degree = position[0]
        sign_index = int(degree // 30)  # Each sign spans 30 degrees
        sign = indian_zodiac[sign_index]  # Indian name + Western equivalent

        # Determine the house for the planet
        house = 1
        for i in range(12):
            next_cusp = house_positions[(i + 1) % 12]
            if (house_positions[i] <= degree < next_cusp) or \
               (house_positions[i] > next_cusp and (degree >= house_positions[i] or degree < next_cusp)):
                house = i + 1
                break

        # Add result for the planet
        results.append({
            'planet': planet_name,
            'degree': round(degree, 2),
            'rashi': sign,
            'house': house
        })

    # Ascendant details
    ascendant_sign = indian_zodiac[int(ascendant // 30)]
    results.insert(0, {
        'ascendant_degree': round(ascendant, 2),
        'ascendant_rashi': ascendant_sign
    })

    return results

def get_birth_transit(dob, tob, pob):
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    results = geocoder.geocode(pob)

    if results and len(results):
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
    else:
        raise ValueError('Location not found')

    sidereal_data_with_houses = calculate_sidereal_positions_with_houses(dob, tob, latitude, longitude)

    output = {
        "location": pob,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude
        },
        "timestamp": f"{dob} {tob}",
        "positions": sidereal_data_with_houses
    }

    return json.dumps(output, indent=2)

# Example usage
# birthtransit = get_birth_transit("2000-01-01", "12:00", "Mumbai, India")
