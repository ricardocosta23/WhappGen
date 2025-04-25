import math
from PIL import Image, ImageDraw

# Create a new image with a white background
size = 48
img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Draw a green chat bubble
bubble_color = (37, 211, 102)  # WhatsApp green
radius = size // 2 - 4
d.ellipse((4, 4, size - 4, size - 4), fill=bubble_color)

# Draw a simplified phone icon in white
phone_color = (255, 255, 255)
d.rectangle((size // 3, size // 3, 2 * size // 3, 2 * size // 3), fill=phone_color)

# Save as PNG
img.save('generated-icon.png')
print("Icon generated: generated-icon.png")
