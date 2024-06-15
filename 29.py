import pandas as pd

# 读取Excel文件
df = pd.read_excel('updated_output1.xlsx')

# 目标网站名列表
target_websites = ['GitLab', 'Reddit', 'Magento', 'One Stop Market']  # 可根据实际需要调整

# 初始化一个字典来存储每个网站的出现次数
counts = {website: 0 for website in target_websites}

# 遍历每行，检查Website Relevance列是否包含任一目标网站名
for index, row in df.iterrows():
    if any(website in row['Website Relevance'] for website in target_websites):
        for website in target_websites:
            if website in row['Website Relevance']:
                counts[website] += 1

# 打印每个网站的计数
print("Counts of website names in 'Website Relevance' column on the same row:")
for website, count in counts.items():
    print(f"{website}: {count}")
