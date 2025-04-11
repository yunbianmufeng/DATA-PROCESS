import io
import json
import sys

# def enrich_data(input_file, output_file):
#     try:
#         with open(input_file, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#
#         enriched_data = []
#         for item in data:
#             if 'name' in item:
#                 item['enriched_info'] = len(item['name'])
#             enriched_data.append(item)
#
#         with open(output_file, 'w', encoding='utf-8') as out_file:
#             json.dump(enriched_data, out_file, ensure_ascii=False, indent=4)
#
#         print(f"数据丰富完成，已保存到 {output_file}")
#     except FileNotFoundError:
#         print(f"错误：未找到输入文件 {input_file}")
#     except json.JSONDecodeError:
#         print(f"错误：无法将输入文件解析为 JSON 格式，请检查文件内容。")
#     except Exception as e:
#         print(f"处理文件时出现错误: {e}")
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='数据丰富脚本')
#     parser.add_argument('--input_file', required=True, help='待丰富的数据文件路径。')
#     parser.add_argument('--output_file', required=True, help='丰富后数据保存的文件路径。')
#     args = parser.parse_args()
#
#     input_file = args.input_file
#     output_file = args.output_file
#
#     enrich_data(input_file, output_file)



def data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#企业名称：", data["name"])

    company = data["company"]
    print(f"#{data["name"]}基本信息：")
    if "start_date" in company:
        print("  注册时间：", company["start_date"])
    if "invest_date" in company:
        print("  投资时间：", company["invest_date"])
    if "scope" in company:
        print("  主营业务：", company["scope"])
    if "address" in company:
        print("  注册地址：", company["address"])

    capital = data["capital"]
    print(f"#{data["name"]}资本结构：")
    print("  股权结构：")
    if "partners" in capital:
        for partner in capital["partners"]:
            print(f"    投资人：{partner['stock_name']}，股权占比：{partner['stock_percent']}%")

    print("  董监高情况：")
    if "employees" in capital:
        for employee in capital["employees"]:
            print(f"    职位：{employee['job']}，姓名：{employee['name']}")

    if "regist_capi" in capital:
        print(f"  注册资金：{capital['regist_capi']} 万元")

    performance = data["performance"]
    print(f"#{data["name"]}经营绩效：")
    if "revenue_tax" in performance:
        for revenue_tax in performance["revenue_tax"]:
            if "tax" in revenue_tax:
                print(f"  纳税：{revenue_tax['tax']} 万元")
            if "year" in revenue_tax:
                print(f"  月份：{revenue_tax['year']}")
            if "profit" in revenue_tax:
                print(f"  利润：{revenue_tax['profit']} 万元")
            if "quarter" in revenue_tax:
                print(f"  季度：{revenue_tax['quarter']}")
            if "revenue" in revenue_tax:
                print(f"  营业收入：{revenue_tax['revenue']} 万元")


    if "innovation_outcomes" in data:
        innovation_outcomes = data["innovation_outcomes"]
        print(f"#{data["name"]}创新成果：")
        if innovation_outcomes is not None and 'intellectual_properties' in innovation_outcomes:
            intellectual_properties = innovation_outcomes["intellectual_properties"]
            for ip in intellectual_properties:
                print(f"  编号：{ip['no']}")
                print(f"  名称：{ip['name']}")
                print(f"  类别：{ip['ip_type']}")
                print(f"  获得时间：{ip['publish_date']}")

    sys.stdout = old_stdout
    data1 = buffer.getvalue()
    buffer.close()
    return data1