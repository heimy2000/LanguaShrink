import pandas as pd
import re  # Importing the regular expressions library

def count_score(prediction, ground_truth):
    # Ensure ground_truth is interpreted correctly by evaluating it (assuming it's a valid Python list in string form)
    try:
        ground_truth_eval = eval(ground_truth)
    except:
        ground_truth_eval = []

    # Convert prediction to string to avoid TypeError
    prediction = str(prediction)
    numbers = re.findall(r"\d+", prediction)
    right_num = 0
    for number in numbers:
        if number in ground_truth_eval:
            right_num += 1
    final_score = 0.0 if len(numbers) == 0 else right_num / len(numbers)
    return float(final_score)

def read_excel_predict(filename):
    data = pd.read_excel(filename, engine='openpyxl')
    total_score = 0

    if 'response' in data.columns and 'answers' in data.columns:
        for index, row in data.iterrows():
            prediction = row['response']
            ground_truth = row['answers']
            score = count_score(prediction, ground_truth)
            total_score += score
            print(f"Row {index + 1}: Prediction: {prediction}, Ground Truth: {ground_truth}, Score: {score}")

        print(f"Total Score: {total_score}")
    else:
        print("Error: The required columns are not in the dataframe.")

# Specify the file path when calling the function
read_excel_predict('passage_count1.xlsx')
