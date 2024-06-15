import pandas as pd
import re

def normalize_answer(s):
    """Normalize answer strings by removing extra spaces, punctuation, and articles."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punct(text):
        return re.sub(r'[^\w\s]', '', text)
    return white_space_fix(remove_articles(remove_punct(s.lower())))

def calculate_f1_score(prediction_tokens, ground_truth_tokens):
    """Calculate the F1 score from prediction and ground truth tokens."""
    common_tokens = set(prediction_tokens).intersection(set(ground_truth_tokens))
    if not prediction_tokens or not ground_truth_tokens:
        return 0.0
    precision = len(common_tokens) / len(prediction_tokens)
    recall = len(common_tokens) / len(ground_truth_tokens)
    if (precision + recall) == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def compute_qa_f1_score(prediction, ground_truth):
    """Compute the QA F1 score for a given prediction and ground truth."""
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)
    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    return calculate_f1_score(prediction_tokens, ground_truth_tokens)

# Load the Excel file
data_frame = pd.read_excel('hotqa1_bm25.xlsx', engine='openpyxl')

# Calculate the F1 score for each row
data_frame['f1_score'] = data_frame.apply(lambda row: compute_qa_f1_score(row['response'], row['answers']), axis=1)

# Calculate the average F1 score
average_f1 = data_frame['f1_score'].mean()

# Print the average F1 score
print("Average F1 Score:", average_f1)
