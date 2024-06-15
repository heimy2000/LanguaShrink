from rank_bm25 import BM25Okapi
import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('hotqa.xlsx')

# 假设 context 列已经是预处理好的分词列表
tokenized_corpus = [doc.split() for doc in df['context']]
bm25 = BM25Okapi(tokenized_corpus)

def generate_response_bm25(query):
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    best_doc = df['context'][scores.argmax()]
    return best_doc

# 应用函数，生成回答，并创建新列
df['response'] = df.apply(lambda row: generate_response_bm25(row['input_']), axis=1)

# 将结果写回新的 Excel 文件
df.to_excel('hotqa1_bm25.xlsx', index=False)
