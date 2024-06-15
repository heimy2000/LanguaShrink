import pandas as pd
import openai
import time

# 设置API密钥
openai.api_base = 'https://one.opengptgod.com/v1'
openai.api_key="sk-stxknfDHd1T3VdeB64E30c45F199430a90A692CcA0359eFe"


def generate_sentence_from_word(word, model="gpt-3.5-turbo"):
    try:
        # 生成句子的提示
        prompt = f"Based on the following words, generate an explanation for this word, which must include subject verb object, adjective and other modifying elements: '{word}':"

        # 调用OpenAI API生成句子
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # 返回生成的句子
        return response['choices'][0]['message']['content']

    except openai.error.RateLimitError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        generate_sentence_from_word(word, model="gpt-3.5-turbo")

    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service is unavailable. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        generate_sentence_from_word(word, model="gpt-3.5-turbo")

    except openai.error.APIError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"API error occurred. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        generate_sentence_from_word(word, model="gpt-3.5-turbo")

    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        generate_sentence_from_word(word, model="gpt-3.5-turbo")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# 读取xlsx文件的第一列
def read_words_from_xlsx(file_path):
    try:
        # 读取xlsx文件的第一列
        df = pd.read_excel(file_path)
        words = df.iloc[:, 0].tolist()
        return words, df
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


# 示例调用
# 示例调用
file_path = "The Oxford 3000.xlsx"
words, df = read_words_from_xlsx(file_path)
if words:
    sentences = []
    for word in words:
        sentence = generate_sentence_from_word(word)
        sentences.append(sentence)

    # 添加生成的句子到DataFrame的第三列
    df['Generated Sentence'] = sentences

    # 保存DataFrame到新的Excel文件
    new_file_path = "Generated_sentences.xlsx"
    df.to_excel(new_file_path, index=False)
    print(f"Generated sentences saved to '{new_file_path}' successfully.")
else:
    print("Failed to read words from the file.")