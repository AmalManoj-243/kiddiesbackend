import cv2
import numpy as np
import os

# Path to the input image
input_path = r"C:\Users\sulab\Desktop\djnago-bookmyshow-clone-master\media\movies\apple-439397_640.webp"
# Output path for the outline image
output_path = r"C:\Users\sulab\Desktop\djnago-bookmyshow-clone-master\media\movies\apple-439397_640_outline.png"

# Read the image
image = cv2.imread(input_path)
if image is None:
    raise FileNotFoundError(f"Image not found: {input_path}")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Invert edges for better visibility (optional)
inverted_edges = cv2.bitwise_not(edges)

# Save the outline image
cv2.imwrite(output_path, inverted_edges)

print(f"Outline saved to: {output_path}")
