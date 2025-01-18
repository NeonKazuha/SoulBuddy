import math
from PIL import Image, ImageDraw

def create_simple_kundli(output_path="simple_kundli.png"):
    # Create a blank image with white background
    width = 800
    height = 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Define the main rectangle dimensions
    margin = 100
    rect_width = width - (2 * margin)
    rect_height = height - (2 * margin)
    
    # Draw the main rectangle
    draw.rectangle(
        [(margin, margin), (width - margin, height - margin)],
        outline="black",
        width=3
    )
    
    # Calculate points for internal lines
    # Vertical lines - divide into three equal parts
    x1 = margin + (rect_width / 3)
    x2 = margin + (2 * rect_width / 3)
    
    # Horizontal lines - divide into three equal parts
    y1 = margin + (rect_height / 3)
    y2 = margin + (2 * rect_height / 3)
    
    # Draw vertical lines
    draw.line([(x1, margin), (x1, height - margin)], fill="black", width=2)
    draw.line([(x2, margin), (x2, height - margin)], fill="black", width=2)
    
    # Draw horizontal lines
    draw.line([(margin, y1), (width - margin, y1)], fill="black", width=2)
    draw.line([(margin, y2), (width - margin, y2)], fill="black", width=2)
    
    # Draw diagonal lines
    draw.line([(margin, margin), (width - margin, height - margin)], fill="black", width=2)
    draw.line([(margin, height - margin), (width - margin, margin)], fill="black", width=2)
    
    # Save the image
    image.save(output_path)
    print(f"Simple Kundli layout saved as {output_path}")
    return image

if __name__ == "__main__":
    create_simple_kundli()