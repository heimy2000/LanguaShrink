from pathlib import Path
import pyarrow as pa
import pandas as pd

# 设置要遍历的文件夹路径
folder_path = 'E:/THUDM_LongBench'

# 遍历文件夹中的所有.json文件
for json_file_path in Path(folder_path).rglob('*.json'):
    try:
        # 读取JSON文件为Pandas DataFrame
        df = pd.read_json(json_file_path)

        # 定义CSV文件路径并保存
        csv_file_path = json_file_path.with_suffix('.csv')
        df.to_csv(csv_file_path, index=False)

        print(f"文件 {json_file_path} 成功转换为CSV.")
    except Exception as e:
        print(f"转换文件 {json_file_path} 到CSV失败: {e}")
