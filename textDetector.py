from PIL import Image
import pytesseract

# Load an image
img = Image.open(r"C:\ProjectAssets - Python\textComplicated.png")

# Extract text from image
text = pytesseract.image_to_string(img)

print(text)

class textDetector:
    def __init__(self):
        pass

