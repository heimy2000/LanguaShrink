import random


def delete_random_words(text, percentage=50):
    # 分割文本为单词列表
    words = text.split()

    # 计算要删除的单词数量
    num_words_to_delete = int(len(words) * (percentage / 100))

    # 随机选择并删除指定数量的单词
    for _ in range(num_words_to_delete):
        if words:  # 检查列表是否为空
            words.pop(random.randrange(len(words)))

    # 将剩余的单词重新组合成字符串
    return ' '.join(words)


# 示例文本
text = "Okay. Thank you. Next step is we're going to do item number, is it that was 16. So I could do item 16. We'll try to get through these as expeditiously as possible. And there's going to be a a motion that's ready to go here. So can we the the the item please. Report from city clerk recommendation to receive and file the certification of the petition regarding the regulation of medical marijuana businesses and approve one of the following three alternative actions adopt the initiative ordinance without alteration to submit the initiative ordinance without alteration to the voters to be held on November 8th, 2016 or three. Adopt a report pursuant to California State Elections Code. Thank you. There's a motion and a second device. Marie Lowenthal. Thank you."

# 删除文本中 50% 的单词
modified_text = delete_random_words(text, percentage=50)

# 打印结果
print(modified_text)
