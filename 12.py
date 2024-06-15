import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge

csv_file_path = 'output6.csv'
csv_file_output_path = 'wikmqa.csv'


# 计算余弦相似度的函数
def calculate_cosine_similarity(original, compressed):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([original, compressed])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]


# 计算BLEU分数的函数，使用平滑函数
def calculate_bleu_score(original, compressed):
    reference = [original.split()]
    hypothesis = compressed.split()
    smoothing = SmoothingFunction().method1
    return sentence_bleu(reference, hypothesis, smoothing_function=smoothing)


# 计算ROUGE分数的函数
def calculate_rouge_score(original, compressed):
    rouge = Rouge()
    scores = rouge.get_scores(compressed, original, avg=True)
    return scores


# 初始化用于累加分数的变量
total_cosine_similarity = 0
total_bleu_score = 0
total_rouge_score = {'rouge-1': {'f': 0, 'p': 0, 'r': 0},
                     'rouge-2': {'f': 0, 'p': 0, 'r': 0},
                     'rouge-l': {'f': 0, 'p': 0, 'r': 0}}
num_entries = 0

# 读取CSV文件、计算得分，并将得分写入新的CSV文件
with open(csv_file_path, 'r', encoding='GB2312',errors='ignore') as csvfile, open(csv_file_output_path, 'w', newline='',
                                                                 encoding='utf-8') as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['cosine_similarity', 'bleu_score', 'rouge-1_f', 'rouge-2_f', 'rouge-l_f']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        original_text = row['label'].strip()
        compressed_text = row['predict'].strip()

        # 检查原文或压缩文本是否为空
        if not original_text or not compressed_text:
            print("Warning: Empty original or compressed text encountered. Skipping.")
            continue

        # 计算分数
        cosine_similarity_score = calculate_cosine_similarity(original_text, compressed_text)
        bleu_score = calculate_bleu_score(original_text, compressed_text)
        try:
            rouge_scores = calculate_rouge_score(original_text, compressed_text)
        except ValueError:
            print(f"Skipping ROUGE calculation due to empty hypothesis for: {row}")
            rouge_scores = {'rouge-1': {'f': 0.0, 'p': 0.0, 'r': 0.0}, 'rouge-2': {'f': 0.0, 'p': 0.0, 'r': 0.0},
                            'rouge-l': {'f': 0.0, 'p': 0.0, 'r': 0.0}}

        # 累加分数
        total_cosine_similarity += cosine_similarity_score
        total_bleu_score += bleu_score
        for key in total_rouge_score.keys():
            total_rouge_score[key]['f'] += rouge_scores[key]['f']
            total_rouge_score[key]['p'] += rouge_scores[key]['p']
            total_rouge_score[key]['r'] += rouge_scores[key]['r']

        num_entries += 1

        # 写入原始数据及其新分数
        row.update({
            'cosine_similarity': cosine_similarity_score,
            'bleu_score': bleu_score,
            'rouge-1_f': rouge_scores['rouge-1']['f'],
            'rouge-2_f': rouge_scores['rouge-2']['f'],
            'rouge-l_f': rouge_scores['rouge-l']['f']
        })
        writer.writerow(row)

# 计算平均分数
average_cosine_similarity = total_cosine_similarity / num_entries
average_bleu_score = total_bleu_score / num_entries
average_rouge_score = {key: {'f': total_rouge_score[key]['f'] / num_entries,
                             'p': total_rouge_score[key]['p'] / num_entries,
                             'r': total_rouge_score[key]['r'] / num_entries} for key in total_rouge_score.keys()}

# 打印平均分数
print(f"平均余弦相似度: {average_cosine_similarity}")
print(f"平均BLEU分数: {average_bleu_score}")
print("平均ROUGE分数:")
for key, scores in average_rouge_score.items():
    print(f"{key}: F分数: {scores['f']}, 精确度: {scores['p']}, 召回率: {scores['r']}")


