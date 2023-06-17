import pytesseract
import PyPDF2
import cv2
import csv
import re
import sys
from pdf2image import convert_from_path

# Function to extract key-value pairs from image using OCR
def extract_key_value_pairs_from_image(file_path):
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(threshold)

    # Define key-value pattern to capture the complete value until the end of the line
    pattern = r'([A-Za-z ]+):([\s\S]+?(?=$|[\r\n]))'
    matches = re.findall(pattern, text)

    # Convert matches to dictionary
    key_value_pairs = {key.strip(): value.strip() for key, value in matches}
    return key_value_pairs

# Function to extract key-value pairs from PDF using PyPDF2
# def extract_key_value_pairs_from_pdf(file_path):
#     key_value_pairs = {}
#     with open(file_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]
#             text = page.extract_text()
#             matches = re.findall(r'([A-Za-z ]+):([\s\S]+?(?=$|[\r\n]))', text)
#             for key, value in matches:
#                 key_value_pairs[key.strip()] = value.strip()
#     return key_value_pairs

def convert_pdf_to_jpg(file_path):
    images = convert_from_path(file_path, first_page=0, last_page=1)  # Convert only the first page
    image_files = []
    for i, image in enumerate(images):
        image_file = f"temp_{i}.jpg"
        image.save(image_file, 'JPEG')
        image_files.append(image_file)
    return image_files[0]

# Function to write key-value pairs to CSV file
def write_key_value_pairs_to_csv(data, csv_path):
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Value'])  # Write header
        for key, value in data.items():
            writer.writerow([key, value])

# Example usage
file_path = sys.argv[1]
output_csv_path = 'output.csv'

# Determine file type and call the appropriate function
if file_path.lower().endswith(('.jpg', '.png','JPEG')):
    key_value_pairs = extract_key_value_pairs_from_image(file_path)
elif file_path.lower().endswith('.pdf'):
    file_path_new=convert_pdf_to_jpg(file_path)
    key_value_pairs = extract_key_value_pairs_from_image(file_path_new)
else:
    print("Unsupported file format")
    sys.exit(1)

print("Key-Value Pairs:")
for key, value in key_value_pairs.items():
    print(f"{key}: {value}")

# Write key-value pairs to CSV file
write_key_value_pairs_to_csv(key_value_pairs, output_csv_path)
print(f"Key-Value pairs written to CSV: {output_csv_path}")
