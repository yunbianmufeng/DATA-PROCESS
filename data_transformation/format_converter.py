import argparse
import csv
import json

def csv_to_json(input_file, output_file):
    data = []
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        print(f"数据已从 CSV 转换为 JSON 并保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")

def json_to_csv(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        if data:
            headers = data[0].keys()
            with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"数据已从 JSON 转换为 CSV 并保存到 {output_file}")
        else:
            print("输入的 JSON 文件为空。")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")

def convert_format(input_file, output_file, input_format, output_format):
    if input_format == 'csv' and output_format == 'json':
        csv_to_json(input_file, output_file)
    elif input_format == 'json' and output_format == 'csv':
        json_to_csv(input_file, output_file)
    else:
        print("不支持的格式转换，请使用 'csv' 到 'json' 或 'json' 到 'csv' 的转换。")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='数据格式转换脚本')
    # parser.add_argument('--input_file', required=True, help='输入数据文件的路径。')
    # parser.add_argument('--output_file', required=True, help='输出数据文件的路径。')
    # parser.add_argument('--input_format', required=True, help='输入数据的格式。')
    # parser.add_argument('--output_format', required=True, help='输出数据的格式。')
    # args = parser.parse_args()
    #
    # input_file = args.input_file
    # output_file = args.output_file
    # input_format = args.input_format
    # output_format = args.output_format
    #
    # convert_format(input_file, output_file, input_format, output_format)

    input_file = input('请输入数据文件的路径（不输入默认为当前项目所在路径）：')
    input_format = input('输入数据的格式（如**.json就直接输入json）：')
    output_file = input('数据输出路径：')
    output_format = input('输出数据的格式：')
    convert_format(input_file, output_file, input_format, output_format)