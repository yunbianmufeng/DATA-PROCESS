# 文件路径
file_path = "C:/Users/Administrator/Desktop/AI/companyData/海研芯（青岛）微电子有限公司.txt"  # 替换为实际文件路径

char_count = 0
in_section = False

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        if line.startswith("##"):
            if in_section:
                print(f"字符数: {char_count}")
                char_count = 0
                if char_count > 500:
                    change_char(line)
            in_section = True
        if in_section:
            char_count += len(line.strip())  # 去掉换行符后计算字符数

if in_section:
    print(f"字符数: {char_count}")

