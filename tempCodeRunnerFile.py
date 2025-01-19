import requests
from PIL import Image, ImageDraw, ImageFont
import math

# Vedicastro API details
API_URL = "https://vedicastroapi.com/api/v1"
API_KEY = "27f92dcf-7901-547f-8205-7704739b3337"  # Replace with your actual API key

# Birth details
data = {