import pandas as pd

import pandas as pd


def classification_score(prediction, ground_truth):
    # 将预测结果和实际答案都转换为小写，并通过逗号分隔成列表
    pred_list = [item.strip().lower() for item in prediction.split('、')]
    gt_list = [item.strip().lower() for item in ground_truth.strip("[]").replace("'", "").split('、')]

    # 计算得分：如果预测列表中的所有项都在实际答案列表中，则得1分，否则得0分
    if all(item in gt_list for item in pred_list) and all(item in pred_list for item in gt_list):
        score = 1.0
    else:
        score = 0.0

    return score


def read_excel_predict(filename):
    # 读取Excel文件
    data = pd.read_excel(filename, engine='openpyxl')

    # 初始化总分
    total_score = 0

    # 检查所需的列是否在数据中
    if 'response' in data.columns and 'answers' in data.columns:
        # 遍历每一行数据
        for index, row in data.iterrows():
            prediction = row['response']
            ground_truth = row['answers']
            # 调用classification_score函数进行评分
            score = classification_score(prediction, ground_truth)
            # 累加得分
            total_score += score
            print(f"Row {index + 1}: Prediction: {prediction}, Ground Truth: {ground_truth}, Score: {score}")

        # 输出总分
        print(f"Total Score: {total_score}")
    else:
        print("Error: The required columns are not in the dataframe.")

# 调用函数，指定文件路径
read_excel_predict('trec3.xlsx')
