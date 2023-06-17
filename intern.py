import pytesseract
from PIL import Image
import cv2
import csv
import re
import tabula

# Function to extract key-value pairs from text using regex pattern matching
def extract_key_value_pairs_from_text(text):
    pattern = r'([A-Za-z ]+):([A-Za-z0-9 ]+)'
    matches = re.findall(pattern, text)
    key_value_pairs = {key.strip(): value.strip() for key, value in matches}
    return key_value_pairs

# Function to extract tables from PDF/image using tabula
def extract_tables(file_path):
    tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True, java_options="-Djava.awt.headless=true")

    return tables

# Function to convert table to CSV
def convert_table_to_csv(table, csv_path):
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table)

# Function to write key-value pairs to CSV file
def write_key_value_pairs_to_csv(data, csv_path):
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Value'])  # Write header
        for key, value in data.items():
            writer.writerow([key, value])

# Example usage
file_path = 'sample1.png'
output_csv_path = 'output.csv'

# Extract text from PDF/image using OCR
image = cv2.imread(file_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
text = pytesseract.image_to_string(threshold)

# Extract key-value pairs from text
text_key_value_pairs = extract_key_value_pairs_from_text(text)
print("Key-Value Pairs from Text:")
for key, value in text_key_value_pairs.items():
    print(f"{key}: {value}")

# Extract tables from PDF/image
pdf_tables = extract_tables(file_path)
print("Tables from PDF/Image:")
for i, table in enumerate(pdf_tables):
    print(f"Table {i+1}:")
    print(table)

# Write key-value pairs to CSV file
write_key_value_pairs_to_csv(text_key_value_pairs, output_csv_path)
print(f"Key-Value pairs from text written to CSV: {output_csv_path}")

# Convert tables to CSV files
for i, table in enumerate(pdf_tables):
    table_csv_path = f"table_{i+1}.csv"
    convert_table_to_csv(table, table_csv_path)
    print(f"Table {i+1} written to CSV: {table_csv_path}")
