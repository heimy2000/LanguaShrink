import csv
import json

# Assuming the JSONL file is named 'input.jsonl' and is located in the same directory as your script.
jsonl_file_path = 'generated_predictions (6).jsonl'
csv_file_path = 'output6.csv'

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['label', 'predict'])  # Write the header row

    # Open the JSONL file and process each line
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            # Load the JSON object from the line
            json_obj = json.loads(line)

            # Extract the 'label' and 'predict' fields and write them to the CSV
            csv_writer.writerow([json_obj['label'], json_obj['predict']])
