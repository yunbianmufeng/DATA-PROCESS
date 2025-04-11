# 文本数据清洗脚本
import argparse
import re


def clean_text(text):
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    # 去除特殊字符，这里保留字母、数字、中文和常见标点
    text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5，。！？：；、,.!?;: ]', '', text)
    return text


def clean_and_save(input_file, output_file):
    try:
        # 读取输入文件内容
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # 清洗文本
        cleaned_text = clean_text(content)

        # 将清洗后的文本保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(cleaned_text)

        print(f"文本清洗完成，已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='文本数据清洗脚本')
    parser.add_argument('--input_file', required=True, help='待清洗的文本数据文件路径。')
    parser.add_argument('--output_file', required=True, help='清洗后文本数据保存的文件路径。')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    clean_and_save(input_file, output_file)
