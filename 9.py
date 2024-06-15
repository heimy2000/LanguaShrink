from datasets import load_dataset

# 加载数据集并传递trust_remote_code=True
dataset = load_dataset("THUDM/LongBench", trust_remote_code=True)


dataset.save_to_disk("E:\11daima")
