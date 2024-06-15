import openai
import pandas as pd
import time

# 不推荐直接在代码中硬编码 API 密钥，应考虑使用环境变量等安全方式
#openai.api_base = 'https://api.pumpkinaigc.online/v1'
openai.api_key = ""

# 读取 Excel 文件
df = pd.read_excel('train-00000-of-00001 (2).xlsx')

def check_website_relevance(context):
    prompt = f"Check if the following sentence is related to any of these websites: GitLab, Reddit, Magento, One Stop Market.\n\nSentence: {context}\n\nWebsites: GitLab, Reddit, Magento, One Stop Market.You can only answer the following four words：GitLab, Reddit, Magento, One Stop Market"

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
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
        return check_website_relevance(context)
    except openai.error.ServiceUnavailableError:
        retry_time = 10  # Adjust the retry time as needed
        print("Service is unavailable. Retrying...")
        time.sleep(retry_time)
        return check_website_relevance(context)
    except openai.error.APIError as e:
        retry_time = 30  # Fallback retry time
        print(f"API error occurred: {e}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return check_website_relevance(context)
    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying...")
        time.sleep(retry_time)
        return check_website_relevance(context)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An error occurred while processing your request."

# 应用函数，生成回答，并创建新列
df['Website Relevance'] = df['generated_task'].apply(check_website_relevance)

# 将结果写回新的 Excel 文件
df.to_excel('updated_output3.xlsx', index=False)