import pandas as pd
from rouge import Rouge
def rouge_score(prediction, ground_truth, **kwargs):
    rouge = Rouge()
    try:
        scores = rouge.get_scores([prediction], [ground_truth], avg=True)
    except:
        return 0.0
    return scores["rouge-l"]["f"]

def read_data(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, engine='openpyxl')
    return df


def calculate_rouge_scores(df):
    scores = []
    for index, row in df.iterrows():
        original, summary = row['answers'], row['response']
        score = rouge_score(original, summary)  # 假设这个函数返回一个得分字典或单一分数
        scores.append(score)
    return scores


def main():
    file_path = 'grep1.xlsx'  # 更新为你的文件路径
    df = read_data(file_path)
    rouge_scores = calculate_rouge_scores(df)

    # 如果 rouge_score 返回的是字典，这里可能需要适当调整
    average_score = pd.Series(rouge_scores).mean()  # 计算平均分
    print(f'Average ROUGE Score: {average_score}')


if __name__ == "__main__":
    main()
