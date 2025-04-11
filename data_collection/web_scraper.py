# 网页数据抓取脚本
import requests
from bs4 import BeautifulSoup
import os
import re

# def scrape_webpage(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         text_content = soup.get_text()
#         return text_content
#     except requests.RequestException as e:
#         print(f"请求网页时出现错误: {e}")
#         return None
#     except Exception as e:
#         print(f"处理网页内容时出现错误: {e}")
#         return None
#
# def save_to_file(content, output_file):
#     try:
#         with open(output_file, 'w', encoding='utf-8') as file:
#             file.write(content)
#         print(f"数据已成功保存到 {output_file}")
#     except Exception as e:
#         print(f"保存文件时出现错误: {e}")
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='网页数据抓取脚本')
#     parser.add_argument('--url', required=True, help='要抓取的网页 URL')
#     parser.add_argument('--output_file', required=True, help='抓取数据保存的文件路径')
#     args = parser.parse_args()
#
#     url = args.url
#     output_file = args.output_file
#
#     scraped_content = scrape_webpage(url)
#     if scraped_content:
#         save_to_file(scraped_content, output_file)

def scrape_and_save(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()

        valid_filename = re.sub(r'[\/:*?"<>|]', '_', url)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        data_warehouse_dir = os.path.join(script_dir, '..', 'data_web_warehouse')

        if not os.path.exists(data_warehouse_dir):
            os.makedirs(data_warehouse_dir)

        output_file = os.path.join(data_warehouse_dir, f'{valid_filename}.txt')

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"数据已成功保存到 {output_file}")
    except requests.RequestException as e:
        print(f"请求网页时出现错误: {e}")
    except Exception as e:
        print(f"处理或保存文件时出现错误: {e}")

def web_scrape(url):
    scrape_and_save(url)

if __name__ == "__main__":
    url = input("请输入要爬取的网页 URL: ")
    scrape_and_save(url)

