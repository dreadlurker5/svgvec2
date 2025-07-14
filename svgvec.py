import requests
from io import BytesIO
from PIL import Image

def image_to_svg(url, threshold=128):
    # Download image
    response = requests.get(url)
    response.raise_for_status()

    # Open image with Pillow
    img = Image.open(BytesIO(response.content)).convert('L')  # grayscale

    width, height = img.size
    pixels = img.load()

    svg_parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}">'.format(width, height),
        '<rect width="100%" height="100%" fill="white"/>'
    ]

    # For simplicity, draw black rects for pixels below threshold
    for y in range(height):
        for x in range(width):
            if pixels[x, y] < threshold:
                svg_parts.append('<rect x="{0}" y="{1}" width="1" height="1" fill="black"/>'.format(x, y))

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)
