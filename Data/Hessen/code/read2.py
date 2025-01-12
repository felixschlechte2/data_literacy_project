import pytesseract
from PIL import Image
import cv2

# Preprocess the image (similar to above)
image = cv2.imread("Versuch.pdf")
if not image:
    print("1")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Perform OCR with Tesseract
text = pytesseract.image_to_string(thresh, lang='deu')  # Use German language model
print(text)
