import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge

# Reading the .xlsx file
df = pd.read_excel('qwen1_arxiv_compress - 副本.xlsx')

# Replacing NaN values with an empty string
df.fillna('', inplace=True)

# Extracting original and compressed sentences into lists
original_sentences = df.iloc[:, 0].tolist()
compressed_sentences = df.iloc[:, 1].tolist()

# Initializing the TF-IDF Vectorizer with adjusted token pattern and disabling stop words
vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b', stop_words=None)

# Calculating Cosine Similarities
cosine_similarities = []
for original, compressed in zip(original_sentences, compressed_sentences):
    # Check if either string is empty after preprocessing
    if not original.strip() or not compressed.strip():
        print("Skipping due to empty input")
        continue
    tfidf_matrix = vectorizer.fit_transform([original, compressed])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    cosine_similarities.append(cosine_sim)

# Calculating BLEU Scores with smoothing
bleu_scores = []
smoother = SmoothingFunction().method1
for original, compressed in zip(original_sentences, compressed_sentences):
    try:
        original_words = original.split()
        compressed_words = compressed.split()
        score = sentence_bleu([original_words], compressed_words, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoother)
        bleu_scores.append(score)
    except Exception as e:
        print(f"Error calculating BLEU score with smoothing: {e}")

# Calculating ROUGE Scores
rouge_scores = {'rouge-1': [], 'rouge-2': [], 'rouge-l': []}
rouge = Rouge()
for original, compressed in zip(original_sentences, compressed_sentences):
    try:
        if not original or not compressed:
            print("Skipping due to empty string pair")
            continue
        scores = rouge.get_scores([compressed], [original])
        rouge_scores['rouge-1'].append(scores[0]['rouge-1']['f'])
        rouge_scores['rouge-2'].append(scores[0]['rouge-2']['f'])
        rouge_scores['rouge-l'].append(scores[0]['rouge-l']['f'])
    except Exception as e:
        print(f"Detailed error with ROUGE score calculation: {e}, Original: {original}, Compressed: {compressed}")

# Checking for empty lists before calculating averages
average_cosine_similarity = sum(cosine_similarities) / len(cosine_similarities) if cosine_similarities else 'No data'
average_bleu_score = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 'No data'
average_rouge_scores = {key: sum(values) / len(values) if values else 'No data' for key, values in rouge_scores.items()}

# Printing average results
print("Average Cosine Similarity: ", average_cosine_similarity)
print("Average BLEU Score: ", average_bleu_score)
print("Average ROUGE-1 Score: ", average_rouge_scores['rouge-1'])
print("Average ROUGE-2 Score: ", average_rouge_scores['rouge-2'])
print("Average ROUGE-L Score: ", average_rouge_scores['rouge-l'])