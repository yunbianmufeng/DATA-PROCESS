# 文件数据加载脚本（按文件夹读取每个文档）
import os
import argparse

# def load_files(input_folder, output_folder):
#     # 检查输入文件夹是否存在
#     if not os.path.exists(input_folder):
#         print(f"输入文件夹 {input_folder} 不存在。")
#         return
#
#     # 检查输出文件夹是否存在，不存在则创建
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # 遍历输入文件夹中的所有文件
#     for filename in os.listdir(input_folder):
#         input_file_path = os.path.join(input_folder, filename)
#         if os.path.isfile(input_file_path):
#             try:
#                 # 读取文件内容
#                 with open(input_file_path, 'r', encoding='utf-8') as file:
#                     content = file.read()
#
#                 # 这里引入对文件内容的操作方法，如data_cleaning和data_transformation里的操作，或者直接调用updata里的方法上传到知识库中
#                 #
#
#                 # 构建输出文件路径
#                 output_file_path = os.path.join(output_folder, filename)
#
#                 # 保存文件内容到输出文件夹
#                 with open(output_file_path, 'w', encoding='utf-8') as output_file:
#                     output_file.write(content)
#
#                 print(f"成功加载并保存文件: {filename}")
#             except Exception as e:
#                 print(f"处理文件 {filename} 时出现错误: {e}")
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='文件数据加载脚本')
#     parser.add_argument('--input_file', required=True, help='输入文件夹的路径')
#     parser.add_argument('--output_file', required=True, help='加载后数据保存的文件夹路径')
#     args = parser.parse_args()
#
#     input_folder = args.input_file
#     output_folder = args.output_file
#
#     load_files(input_folder, output_folder)




# 指定文件夹路径
folder_path = "C:/Users/Administrator/Desktop/AI/companyData"  # 可替换为其他文件夹路径


def file_loader():
    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为txt文件（可替换为其他类型的文档类型）
        if filename.endswith(".txt"):
            name_without_extension = os.path.splitext(filename)[0]

            file_path = os.path.join(folder_path, filename)
            # 构建完整文件路径
            print(f"\n=== 文件名: {filename} ===")  # 打印文件名

            # 打开并读取文件内容
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.readlines()  # 按行读取内容
                    modified_content = []
                    for line in content:
                        if line.startswith('##'):
                            modified_line = line.replace('##', f'##{name_without_extension}')  # 在 "##" 后面加入文件名并换行
                            modified_content.append(modified_line)
                        else:
                            modified_content.append(line)  # 保持原样

                    # 将修改后的内容写回文件
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.writelines(modified_content)  # 写回文件

                    print("文件修改完成！")


            except UnicodeDecodeError:
                print(f"警告: 文件 {filename} 无法以 UTF-8 编码读取，尝试其他编码...")
                try:
                    with open(file_path, "r", encoding="gbk") as file:
                        content = file.read()
                        print("文件内容：")
                        print(content)
                except Exception as e:
                    print(f"错误: 无法读取文件 {filename}: {str(e)}")
            except Exception as e:
                print(f"错误: 无法读取文件 {filename}: {str(e)}")



