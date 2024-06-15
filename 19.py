import json
import csv

# Open the JSONL file and read lines
with open('generated_predictions (4).jsonl', 'r',encoding='MacRoman') as json_file:
    json_lines = json_file.readlines()

# Assuming all objects have the same structure, get headers from the first JSON object
headers = list(json.loads(json_lines[0]).keys())

# Open or create a CSV file and write data
with open('data4+.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
    csv_writer.writeheader()  # write headers

    for line in json_lines:
        # Convert JSON string to Python dict
        data = json.loads(line)
        csv_writer.writerow(data)  # write data row
