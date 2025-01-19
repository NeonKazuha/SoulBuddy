import requests
from PIL import Image, ImageDraw, ImageFont
import math
from components.FindHoroscope import get_horoscope

# Vedicastro API details
API_URL = "https://vedicastroapi.com/api/v1"
API_KEY = "27f92dcf-7901-547f-8205-7704739b3337"  # Replace with your actual API key

# Birth details
data = {
    "api_key": API_KEY,
    "date": "1995-12-25",    # Date of birth in YYYY-MM-DD
    "time": "14:30",         # Time of birth in HH:MM format (24-hour)
    "latitude": 28.6139,     # Latitude of birth location
    "longitude": 77.2090,    # Longitude of birth location
    "timezone": 5.5          # Timezone offset
}

# Make the API request
response = requests.post(f"{API_URL}/kundli", data=data)

# Initialize kundli_data
kundli_data = None

# Check if the response is valid
if response.status_code == 200:
    try:
        kundli_data = response.json()
    except ValueError:
        print("Error: Response content is not valid JSON.")
        print("Response text:", response.text)  # Print the raw response for debugging
else:
    print(f"Error: Received response with status code {response.status_code}")
    print("Response text:", response.text)  # Print the raw response for debugging

# Check if kundli_data is defined before accessing it
if kundli_data is not None:
    houses = kundli_data.get("houses", [])
    planets = kundli_data.get("planets", [])
    ascendant = kundli_data.get("ascendant", "Unknown")

    # Create a blank Kundli chart
    image = Image.new("RGB", (1000, 1000), "white")
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", size=18)
        title_font = ImageFont.truetype("arial.ttf", size=20)
    except IOError:
        font = ImageFont.load_default()
        title_font = font

    # Draw the Circle (Kundli wheel)
    center = (500, 500)
    radius = 400

    # Draw the outer circle (Kundli wheel)
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="black", width=2)

    # Draw the 12 Houses
    for i in range(12):
        angle = math.radians(i * 30)  # 360 / 12 = 30 degrees per house
        x1 = center[0] + radius * math.cos(angle)
        y1 = center[1] + radius * math.sin(angle)
        x2 = center[0] + (radius - 40) * math.cos(angle)
        y2 = center[1] + (radius - 40) * math.sin(angle)

        draw.line([x1, y1, x2, y2], fill="black", width=2)

    # Mark house numbers and ascendant
    house_positions = []
    for i in range(12):
        angle = math.radians(i * 30)
        x = center[0] + (radius - 20) * math.cos(angle)
        y = center[1] + (radius - 20) * math.sin(angle)
        house_positions.append((x, y))

    # Add House Numbers
    for i, pos in enumerate(house_positions, 1):
        bbox = draw.textbbox((0, 0), str(i), font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((pos[0] - text_width / 2, pos[1] - text_height / 2), str(i), fill="black", font=font)

    # Fill the Houses with Planets
    for planet in planets:
        house = planet.get("house", 1)
        name = planet.get("name", "Unknown")
        rashi = planet.get("rashi", "Unknown")

        # Find the house center
        angle = math.radians((house - 1) * 30)  # house numbers are 1-based
        x = center[0] + (radius - 60) * math.cos(angle)
        y = center[1] + (radius - 60) * math.sin(angle)

        # Draw planet name and Rashi next to it
        text = f"{name} ({rashi})"
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - text_width / 2, y - text_height / 2), text, fill="black", font=font)

    # Save and display the image
    output_path = "kundli_chart_api.png"
    image.save(output_path)
    print(f"Kundli chart saved as {output_path}")
    image.show()

    # Get horoscope if needed
    horoscope = get_horoscope("1995-12-25", "14:30", "28.6139,77.2090", "current_position")
    print("Horoscope:", horoscope)
else:
    print("No valid kundli data available to process.")