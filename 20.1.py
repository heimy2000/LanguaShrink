from pathlib import Path
import pandas as pd
import joblib

# 设置要遍历的文件夹路径
folder_path = 'E:/THUDM_LongBench'

# 遍历文件夹中的所有.joblib文件
for joblib_file_path in Path(folder_path).rglob('*.joblib'):
    try:
        # 使用joblib加载数据
        data = joblib.load(joblib_file_path)

        # 提取数据类型（DataFrame或其他）
        data_type = type(data).__name__

        if data_type == 'DataFrame':
            # 如果数据是DataFrame，则转换为Excel并保存
            excel_output_path = joblib_file_path.with_suffix('.xlsx')
            data.to_excel(excel_output_path, index=False)
            print(f"文件 {joblib_file_path} 成功转换为Excel格式.")
        else:
            print(f"文件 {joblib_file_path} 中的数据类型为 {data_type}，无法转换为Excel格式.")
    except Exception as e:
        print(f"读取文件 {joblib_file_path} 失败: {e}")
