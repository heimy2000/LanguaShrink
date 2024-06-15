import openai
import pandas as pd

# 安全性建议：不要在代码中硬编码 API 密钥，而应考虑使用环境变量等安全方式
openai.api_key = "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"

# 读取 Excel 文件
df = pd.read_excel('quality.xlsx')

def check_website_relevance(row):
    # 直接使用row['input_']作为prompt
    prompt = row['input_'] + "Just answer the answer"

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=100,
            temperature=0,
            top_p=1
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Error"

# 应用函数，生成回答，并创建新列
df['Response'] = df.apply(check_website_relevance, axis=1)

# 将结果写回新的 Excel 文件
df.to_excel('output_file1.xlsx', index=False)
