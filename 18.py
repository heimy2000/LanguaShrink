import pandas as pd
import openai
import time
# 设置OpenAI API密钥
openai.api_base = 'https://one.opengptgod.com/v1'
openai.api_key = "sk-s"

# 读取Excel文件
df = pd.read_excel('multi.xlsx')

# 为了保存压缩后的句子，我们添加一个新列
df['压缩句子'] = ''


def attempt_api_call(question, attempt=1):
    max_attempts = 5  # 最大重试次数
    try:
        # 调用API生成压缩句子
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": question}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response
    except Exception as e:
        print(f"Attempt {attempt}: API call failed with error: {e}")
        if attempt < max_attempts:
            time.sleep(2 ** attempt)  # 指数退避策略
            return attempt_api_call(question, attempt + 1)
        else:
            raise  # 达到最大重试次数后抛出异常


for index, row in df.iterrows():
    # 构建prompt
    question = f'''如果句子中有两个逗号或破折号，删除它们之间的部分。
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

按照上述规则简化句子,尽量保持语义不变。使用英语，只需要保留主谓宾{row['context']}'''

    # 尝试调用API，包含重试逻辑
    try:
        response = attempt_api_call(question)
        compressed_sentence = response['choices'][0]['message']['content']
        df.at[index, '压缩句子'] = compressed_sentence.strip()
    except Exception as final_error:
        print(f"Failed after multiple attempts: {final_error}")
        df.at[index, '压缩句子'] = "API调用失败"
        time.sleep(5)
# 最后，您可以选择保存新的表格到文件
df.to_excel('1231+.xlsx', index=False)