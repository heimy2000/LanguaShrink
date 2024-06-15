import os
import pandas as pd

# 获取当前工作目录
current_folder = os.getcwd()

# 创建一个空的 DataFrame 列表，用于存储所有 Parquet 文件的内容
dfs = []

# 遍历当前文件夹中的所有文件
for filename in os.listdir(current_folder):
    if filename.endswith(".parquet"):
        # 构建 Parquet 文件的完整路径
        parquet_path = os.path.join(current_folder, filename)

        # 读取 Parquet 文件为 DataFrame
        df = pd.read_parquet(parquet_path)

        # 将当前 Parquet 文件的内容添加到 dfs 列表中
        dfs.append(df)

# 合并所有 DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# 将 combined_df 保存为 JSON 文件
combined_df.to_json("1.json", orient="records")
