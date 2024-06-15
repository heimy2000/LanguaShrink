import zlib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# 原始文本和压缩文本
original_text = "Q: I have a blackberry, a clarinet, a nectarine, a plum, a strawberry, a banana, a flute, an orange, and a violin. How many fruits do I have? A: Let's think step by step. We first identify the fruits on the list and include their quantity in parentheses: - blackberry (1) - nectarine (1) - plum (1) - strawberry (1) - banana (1) - orange (1) Now, let's add the numbers in parentheses: 1 + 1 + 1 + 1 + 1 + 1 = 6. So the answer is 6."
compressed_text = "Let's think step by step. We first identify the fruits on the list: blackberry, clarinet, nectarine, plum, strawberry, banana, flute, orange, and violin. Now, let's add the fruits: blackberry, nectarine, plum, strawberry, banana, and orange. So the answer is 6"

# 计算余弦相似度
def calculate_cosine_similarity(original, compressed):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([original, compressed])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

# 计算BLEU分数
def calculate_bleu_score(original, compressed):
    reference = [original.split()]
    hypothesis = compressed.split()
    return sentence_bleu(reference, hypothesis)

# 计算ROUGE分数
def calculate_rouge_score(original, compressed):
    rouge = Rouge()
    scores = rouge.get_scores(compressed, original)
    return scores

# 计算结果
cosine_similarity_score = calculate_cosine_similarity(original_text, compressed_text)
bleu_score = calculate_bleu_score(original_text, compressed_text)
rouge_scores = calculate_rouge_score(original_text, compressed_text)

# 输出结果
print(f"余弦相似度: {cosine_similarity_score}")
print(f"BLEU分数: {bleu_score}")
print(f"ROUGE分数: {rouge_scores}")
