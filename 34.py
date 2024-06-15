import openai
import pandas as pd

# 设定OpenAI的API密钥
openai.api_key = ''

# 使用pandas读取Excel文件
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-0125-preview',  # 使用特定模型
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0,
            top_p=1
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

# 使用pandas读取Excel文件
file_path = 'NQ-open.train.xlsx'
df = pd.read_excel(file_path)

# 确保你的Excel文件中有一个名为'question'的列
if 'question' in df.columns:
    # 创建一个用于存储回答的新列
    df['response'] = ''

    # 遍历每个问题，调用generate_response函数进行回答
    for index, row in df.iterrows():
        # 生成回答
        response_text = generate_response(row['question']+'''如果句子中有两个逗号或破折号，删除它们之间的部分。
如果句子中只有一个逗号后接定语从句，删除定语从句。
删除所有形容词和副词。
记住人名。
删除所有定语、状语和同位语，以及它们的从句。
转折关系处理：转折词前的内容如果与转折词后的内容含义相反，则保留转折词后的内容；否则，转折词之后的内容为重点。
让步关系处理：让步词前后含义相反时，根据让步词的位置决定保留哪部分。
原因关系处理：保留表示原因的部分。
结果关系处理：保留导致结果的原因部分。
条件关系处理：保留表示条件的部分。
递进关系处理：递进词之后的部分通常是重点。
比较关系处理：保留比较的内容，比较的两方面通常具有相反含义。
并列关系处理：并列关系中的部分视为平等，无逻辑重点，保持结构和性质一致。
例子：
原句：“Pushed by science, or what claims to be science, society is reclassifying what once were considered character flaws or moral failings as personality disorders akin to physical disabilities.”
简化后：“Society is reclassifying as personality disorders akin to physical disabilities.”

原句：“The Internet—and pressure from funding agencies, who are questioning why commercial publishers are making money from government-funded research by restricting access to it—is making access to scientific results a reality.”
简化后：“The Internet is making access to scientific results a reality.”

原句：“Clearly, you try to comprehend, in the sense of identifying meanings for individual words and working out relationships between them, drawing on your implicit knowledge of English grammar.”
简化后：“You try to comprehend drawing on your implicit knowledge.”

按照上述规则简化句子,尽量保持语义不变。''')
        # 保存回答到DataFrame
        df.at[index, 'response'] = response_text

    # 将带有回答的DataFrame保存回Excel文件
    df.to_excel('NQ-open.train2.xlsx', index=False)
else:
    print("Error: 'question' column not found in the Excel file.")