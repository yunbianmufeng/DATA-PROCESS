import os

# 指定文件夹路径
folder_path = "C:/Users/Administrator/Desktop/AI/companyData"  # 替换为实际文件夹路径

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    # 检查文件是否为txt文件
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
                        modified_line = line.replace('##', f'##{name_without_extension}')  # 在 "##" 后面加入 "112233" 并换行
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