# 重复数据去除脚本
import argparse
def remove_duplicates(input_file, output_file):
    try:
        # 读取输入文件的所有行
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 去除重复行
        unique_lines = list(set(lines))

        # 将去重后的行写回到输出文件
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.writelines(unique_lines)

        print(f"重复数据去除完成，已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='重复数据去除脚本')
    parser.add_argument('--input_file', required=True, help='包含重复数据的文件路径。')
    parser.add_argument('--output_file', required=True, help='去除重复项后数据保存的文件路径。')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    remove_duplicates(input_file, output_file)
