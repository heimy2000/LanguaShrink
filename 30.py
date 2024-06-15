import openai
import pandas as pd
import time

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = "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"

# Function to check if the sentence is related to any of the specified websites
def check_website_relevance(sentence):
    prompt = f'''如果句子中有两个逗号或破折号，删除它们之间的部分。
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

按照上述规则简化句子,尽量保持语义不变。
句子:''' + sentence

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-turbo-preview',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=100,
            temperature=0,
            top_p=1
        )
        return response.choices[0].message['content']
    except openai.error.RateLimitError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return check_website_relevance(sentence)
    except openai.error.ServiceUnavailableError:
        retry_time = 10  # Adjust the retry time as needed
        print("Service is unavailable. Retrying...")
        time.sleep(retry_time)
        return check_website_relevance(sentence)
    except openai.error.APIError as e:
        retry_time = 30  # Fallback retry time
        print(f"API error occurred: {e}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return check_website_relevance(sentence)
    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying...")
        time.sleep(retry_time)
        return check_website_relevance(sentence)


# Read the Excel file
df = pd.read_excel('grep1.xlsx')

# Apply the function to each row in the 'response' column and save the results in a new column
df['Website Relevance'] = df['response'].apply(check_website_relevance)

# Write the results back to a new Excel file
df.to_excel('grep1outp434ut.xlsx', index=False)

print("Processing complete. The results have been saved in 'grep1output.xlsx'.")

