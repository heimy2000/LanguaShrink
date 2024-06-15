import openai
import pandas as pd
import time

# 不推荐直接在代码中硬编码 API 密钥，应考虑使用环境变量等安全方式
#openai.api_base = 'https://api.pumpkinaigc.online/v1'
openai.api_key = "sk-"

# 读取 Excel 文件
df = pd.read_excel('hotqa.xlsx')

def generate_response(context, input_):
    prompt = f'''Answer the question based on the given passages. Only give me the answer and do not output any other words.\n\nThe following are given passages.\n{context}\n\nAnswer the question based on the given passages. Only give me the answer and do not output any other words.\n\nQuestion: {input_}\nAnswer:'''

#回答问题：{input_text}，请你回答使用英语'''
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens = 4000,
            temperature = 0,
            top_p = 1

        )
        return response.choices[0].message['content']

# 应用函数，生成回答，并创建新列
df['response'] = df.apply(lambda row: generate_response(row['context'], row['input']), axis=1)

# 将结果写回新的 Excel 文件
df.to_excel('hotqa1 .xlsx', index=False)
