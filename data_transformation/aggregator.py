import argparse
import json

def aggregate_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        aggregated_data = {}
        for item in data:
            category = item.get('category')
            value = item.get('value')
            if category is not None and value is not None:
                if category in aggregated_data:
                    aggregated_data[category] += value
                else:
                    aggregated_data[category] = value

        result = [{'category': category, 'total_value': total_value}
                  for category, total_value in aggregated_data.items()]

        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(result, out_file, ensure_ascii=False, indent=4)

        print(f"数据聚合完成，已保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到输入文件 {input_file}")
    except json.JSONDecodeError:
        print(f"错误：无法将输入文件解析为 JSON 格式，请检查文件内容。")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='数据聚合脚本')
    parser.add_argument('--input_file', required=True, help='原始数据文件路径。')
    parser.add_argument('--output_file', required=True, help='聚合后数据保存的文件路径。')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    aggregate_data(input_file, output_file)
