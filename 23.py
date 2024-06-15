import pandas as pd

# 加载xlsx文件
df = pd.read_excel('passage_count1.xlsx')  # 替换为你的文件路径

# 假设我们现在比较 'answers' 列和 'response' 列
count = 0
for index, row in df.iterrows():
    # 假设每个单元格都是字符串形式的列表，先转换为实际的列表
    try:
        answers_list = eval(row['answers'])
        if not isinstance(answers_list, list):
            continue  # 如果转换后不是列表，则跳过当前行
    except:
        continue  # 如果转换出错，跳过当前行

    # 计算每个答案是否出现在 'response' 列中
    if any(answer in row['response'] for answer in answers_list):
        count += 1

print(f"共有 {count} 次 'answers' 列中的元素出现在 'response' 列中。")
