def remove_chinese_characters(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file, \
         open(output_path, 'w', encoding='utf-8') as out_file:
        for line in file:
            # 使用str.isascii()来过滤掉所有非ASCII字符，这包括中文
            filtered_line = ''.join(char for char in line if char.isascii())
            out_file.write(filtered_line)

# 使用示例
remove_chinese_characters('03.txt', '031.txt')
