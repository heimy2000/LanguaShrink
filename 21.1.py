import openai
import pandas as pd
import threading
from queue import Queue

# 设定API密钥
openai.api_key = 's'

# 读取Excel文件
file_path = 'NQ-open.dev.xlsx'
df = pd.read_excel(file_path)

# 创建一个列来保存响应
df['response'] = None

# 工作队列
work_queue = Queue()

# 结果队列
result_queue = Queue()

def worker():
    while not work_queue.empty():
        index, question = work_queue.get()
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4-0125-preview',
                messages=[{'role': 'user', 'content': question}],
                temperature=0,
                top_p=1
            )
            result = response.choices[0].message['content']
        except Exception as e:
            result = str(e)
        result_queue.put((index, result))
        work_queue.task_done()

# 将问题加入工作队列
for index, row in df.iterrows():
    work_queue.put((index, row['question']))

# 启动工作线程
num_threads = 10  # 可以根据情况调整线程数
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# 等待所有任务完成
work_queue.join()

# 从结果队列获取结果并更新DataFrame
while not result_queue.empty():
    index, response = result_queue.get()
    df.at[index, 'response'] = response

# 保存DataFrame回Excel
df.to_excel('NQ-open.dev1-.xlsx', index=False)

# 确保所有线程都已完成
for t in threads:
    t.join()
