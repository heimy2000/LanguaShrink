from pathlib import Path
import pyarrow as pa
import pandas as pd

# 设置要遍历的文件夹路径
folder_path = 'E:/THUDM_LongBench'

# 遍历文件夹中的所有.arrow文件
for arrow_file_path in Path(folder_path).rglob('*.arrow'):
    try:
        # 尝试以Arrow流格式读取文件
        with arrow_file_path.open('rb') as f:
            reader = pa.ipc.open_stream(f)
            table = reader.read_all()

        # 将Arrow表转换为Pandas DataFrame
        df = table.to_pandas()

        # 定义XLSX文件路径并保存
        xlsx_file_path = arrow_file_path.with_suffix('.xlsx')
        df.to_excel(xlsx_file_path, index=False)

        print(f"文件 {arrow_file_path} 成功转换为XLSX.")
    except Exception as e:
        print(f"读取文件 {arrow_file_path} 失败: {e}")
