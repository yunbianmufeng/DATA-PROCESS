# 空值处理脚本
import argparse
import csv

def handle_null_values(input_file, output_file, default_value=''):
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
                open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for row in reader:
                # 处理每行数据，将空值替换为默认值
                new_row = [default_value if value == '' else value for value in row]
                writer.writerow(new_row)

        print(f"空值处理完成，已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")

def handle_null_values_forjson(data, default_value=''):
    try:
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if value == '':
                            item[key] = default_value
        elif isinstance(data, dict):
            for key, value in data.items():
                if value == '':
                    data[key] = default_value
        print("空值处理完成")
        return data
    except Exception as e:
        print(f"处理数据时出现错误: {e}")
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='空值处理脚本')
    parser.add_argument('--input_file', required=True, help='包含空值的数据文件路径。')
    parser.add_argument('--output_file', required=True, help='处理空值后数据保存的文件路径。')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    handle_null_values(input_file, output_file)
