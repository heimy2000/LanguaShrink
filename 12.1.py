import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Excel文件路径
xlsx_file_path = 'qwen0.5B_arxiv_compress.xlsx'

# 读取Excel文件
df = pd.read_excel(xlsx_file_path)

# 初始化一个列表来存储每行的BLEU分数
bleu_scores = []

# 遍历DataFrame中的每一行
for index, row in df.iterrows():
    try:
        # 获取参考句子和候选句子
        reference_sentence = row['text'].split()  # 分割成单词列表
        candidate_sentence = row['CompressedPrompt'].split()  # 分割成单词列表

        # 使用NLTK的sentence_bleu函数计算BLEU分数
        # SmoothingFunction可以是其中一个平滑函数，如Chencherry或Linear
        smoothing_function = SmoothingFunction()
        bleu_score = sentence_bleu([reference_sentence], candidate_sentence,
                                   smoothing_function=smoothing_function.method1)

        # 将计算出的BLEU分数添加到bleu_scores列表中
        bleu_scores.append(bleu_score)
    except Exception as e:
        # 如果发生错误，添加一个占位符或者打印错误信息
        print(f"Error calculating BLEU score for row {index}: {e}")
        bleu_scores.append(None)  # 或者使用其他方式处理错误

# 将BLEU分数添加到DataFrame中
df['BLEU Score'] = bleu_scores

# 显示更新后的DataFrame
print(df.head())