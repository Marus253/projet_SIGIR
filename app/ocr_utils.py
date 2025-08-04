import easyocr
from PIL import Image

reader = easyocr.Reader(['fr'], gpu=False)

def detect_plate_text(image_path):
    results = reader.readtext(image_path)
    for bbox, text, confidence in results:
        if len(text) >= 5 and confidence > 0.5:
            return text.upper().strip()
    return None
