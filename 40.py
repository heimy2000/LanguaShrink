import pandas as pd
import json

# Load JSON file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Convert JSON to Excel
def json_to_excel(json_data, excel_file_path):
    df = pd.DataFrame(json_data)
    df.to_excel(excel_file_path, index=False)

# Main function to convert JSON file to Excel
def convert_json_to_excel(json_file_path, excel_file_path):
    json_data = load_json(json_file_path)
    json_to_excel(json_data, excel_file_path)

# Usage
json_file_path = 'gpt-3.5-turbo_vs_RLapi_k_1_k1.json'  # Replace with your JSON file path
excel_file_path = 'output_fileqwen.xlsx'  # Replace with your desired Excel file path

convert_json_to_excel(json_file_path, excel_file_path)
