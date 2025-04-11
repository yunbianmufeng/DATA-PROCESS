import argparse
import json
import csv


def save_file(input_file, output_file):
    try:
        input_ext = input_file.split('.')[-1].lower()

        if input_ext == 'txt':
            # 处理文本文件
            with open(input_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(content)
            print(f"文本文件数据已成功保存到 {output_file}")

        elif input_ext == 'json':
            # 处理 JSON 文件
            with open(input_file, 'r', encoding='utf-8') as infile:
                data = json.load(infile)
            with open(output_file, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
            print(f"JSON 文件数据已成功保存到 {output_file}")

        elif input_ext == 'csv':
            # 处理 CSV 文件
            with open(input_file, 'r', encoding='utf-8', newline='') as infile:
                reader = csv.reader(infile)
                data = list(reader)
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(data)
            print(f"CSV 文件数据已成功保存到 {output_file}")

        else:
            print(f"不支持的文件类型: {input_ext}，请使用 txt、json 或 csv 文件。")

    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except json.JSONDecodeError:
        print(f"错误：无法将输入的 JSON 文件解析，请检查文件内容。")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='数据保存到本地文件脚本')
    parser.add_argument('--input_file', required=True, help='要保存的数据文件路径。')
    parser.add_argument('--output_file', required=True, help='保存数据的文件路径。')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    save_file(input_file, output_file)
