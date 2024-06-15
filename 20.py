from pathlib import Path
import pyarrow as pa
import pandas as pd

# 设置要遍历的文件夹路径
folder_path = 'E:/THUDM_LongBench'

# 遍历文件夹中的所有.xlsx文件
for xlsx_file_path in Path(folder_path).rglob('*.xlsx'):
    try:
        # 读取XLSX文件为Pandas DataFrame
        df = pd.read_excel(xlsx_file_path)

        # 将DataFrame转换为Arrow表
        table = pa.Table.from_pandas(df)

        # 定义Arrow文件路径并保存
        arrow_file_path = xlsx_file_path.with_suffix('.arrow')
        with arrow_file_path.open('wb') as f:
            writer = pa.ipc.new_stream(f, table.schema)
            writer.write_table(table)
            writer.close()

        print(f"文件 {xlsx_file_path} 成功转换为Arrow格式.")
    except Exception as e:
        print(f"读取文件 {xlsx_file_path} 失败: {e}")
