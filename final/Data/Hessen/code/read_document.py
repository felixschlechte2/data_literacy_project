import easyocr
from pdf2image import convert_from_path
import re
import numpy as np
import cv2

# Path to your PDF file
pdf_path = "Versuch.pdf"

# Step 1: Convert PDF pages to images
images = convert_from_path(pdf_path, dpi = 300)

# Preprocess each page
preprocessed_images = []
for page_num, image in enumerate(images, start=1):
    # Convert PIL image to OpenCV format (NumPy array)
    image_np = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Optional: Remove noise with morphological operations
    kernel = np.ones((2, 2), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Save preprocessed image to the list
    preprocessed_images.append(clean)

# Step 2: Initialize EasyOCR Reader
reader = easyocr.Reader(['de'], gpu=False)  # 'de' for German text recognition
# Step 3: Extract Text from Each Page
for page_num, image in enumerate(preprocessed_images, start=1):

    print(f"Processing page {page_num}...")
    
    # Convert image to NumPy array
    #image_np = np.array(image)
    
    # Perform OCR on the image
     # Perform OCR on the image
    results = reader.readtext(image, detail=0, paragraph=True, min_size=15, text_threshold=0.7, link_threshold=0.5, low_text=0.3)
    page_text = "\n".join(results)  # Combine all text into a single string

    # Step 4: Extract Specific Information Using Regex
    print(f"Extracted Text from Page {page_num}:")
    print(page_text)

    # Regex patterns to match specific fields
    region_pattern = r"Region Hannover"
    cdu_pattern = r"CDU.*?([\d.,]+)\s*%"
    percent_pattern = r"([\d.,]+)\s*%"

    # Match Region Hannover
    if re.search(region_pattern, page_text):
        print("Found Region Hannover")

    # Match CDU percentage
    cdu_match = re.search(cdu_pattern, page_text)
    if cdu_match:
        cdu_percentage = cdu_match.group(1)
        print(f"CDU Percentage: {cdu_percentage} %")

    # Match any percentage
    percentages = re.findall(percent_pattern, page_text)
    if percentages:
        print("All Percentages Found:", percentages)

    print("-" * 50)

# Step 4: Combine and Display Extracted Text
#full_text = "\n".join(all_text)
#print("Extracted Text:")
#print(full_text)

# Step 5: Extract Numbers (Optional)
# Use regex to extract all numbers from the text
#numbers = re.findall(r'\d+[\.,]?\d*', full_text)
#print("Extracted Numbers:")
#print(numbers)
