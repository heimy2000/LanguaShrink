# 导入nltk库
import nltk
nltk.download('punkt')  # 下载punkt tokenizer模型

# 函数：计算文件中的token数量
def count_tokens_with_nltk(file_path):
    try:
        # 打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            content = file.read()
            # 使用nltk的word_tokenize方法分割tokens
            tokens = nltk.word_tokenize(content)
            # 返回token的数量
            return len(tokens)
    except FileNotFoundError:
        return "文件未找到，请检查路径。"
    except Exception as e:
        return f"发生错误：{e}"

# 调用函数
file_path = '2.txt'  # 更换为你的文件路径
print(f"文件中的NLP token数量是：{count_tokens_with_nltk(file_path)}")
