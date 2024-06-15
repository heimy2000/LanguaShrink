from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# 初始化模型和分词器
model_name = 'gpt2'  # 可以替换为其他的模型
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def calculate_perplexity(sentence):
    # 编码并添加特殊的结束标记
    input_ids = tokenizer.encode(sentence, return_tensors='pt')

    # 获取模型的输出（这里忽略了过长序列的处理）
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
    loss = outputs[0]

    # 困惑度是交叉熵损失的指数
    perplexity = torch.exp(loss).item()
    return perplexity


# 计算一个句子的困惑度
sentence = "The quick brown fox jumps over "
perplexity = calculate_perplexity(sentence)
print(f"Perplexity of the sentence is: {perplexity}")
