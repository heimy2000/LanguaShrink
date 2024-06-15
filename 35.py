import pandas as pd
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

# 读取Excel文件
file_path = 'NQ-open.dev.xlsx'
df = pd.read_excel(file_path)

# 检查是否存在'question'列
if 'question' not in df.columns:
    print("Error: 'question' column not found in the Excel file.")
    exit()

# 假设答案存储在'answer'列，如果没有，你需要相应调整
if 'answer' not in df.columns:
    print("Error: 'answer' column not found in the Excel file.")
    exit()

# 对问题进行分词
tokenized_corpus = [word_tokenize(doc) for doc in df['question'].tolist()]
bm25 = BM25Okapi(tokenized_corpus)

# 为每个问题生成一个回答
df['bm25_response'] = ''
for index, row in df.iterrows():
    query = row['question']
    tokenized_query = word_tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    top_index = scores.argmax()  # 获取得分最高的索引
    response_text = df.at[top_index, 'answer']  # 获取对应的答案
    df.at[index, 'bm25_response'] = response_text

# 将带有回答的DataFrame保存回Excel文件
df.to_excel('NNQ-open.dev1.xlsx', index=False)
