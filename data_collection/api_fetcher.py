# API 数据获取脚本
import requests
import argparse
import json

# def fetch_api_data(api_url):
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"请求 API 时出现错误: {e}")
#         return None
#     except ValueError as e:
#         print(f"解析 API 响应为 JSON 时出现错误: {e}")
#         return None
#
# def save_to_file(data, output_file):
#     try:
#         with open(output_file, 'w', encoding='utf-8') as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)
#         print(f"数据已成功保存到 {output_file}")
#     except Exception as e:
#         print(f"保存文件时出现错误: {e}")
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='API 数据获取脚本')
#     parser.add_argument('--api_url', required=True, help='API 的 URL')
#     parser.add_argument('--output_file', required=True, help='获取数据保存的文件路径')
#     args = parser.parse_args()
#
#     api_url = args.api_url
#     output_file = args.output_file
#
#     fetched_data = fetch_api_data(api_url)
#     if fetched_data:
#         save_to_file(fetched_data, output_file)


from utils.get_api_token import get_access_token

# access_token = get_access_token()
# print(access_token)

def access_api(API_ENDPOINT,access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(API_ENDPOINT, headers=headers)
        response.raise_for_status()
        try:
            data = response.json()
            # print("access_api——API响应数据：")
            # print(data)
            return data
        except ValueError:
            print("响应内容（非JSON格式）：")
            # print(response.text)

    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')

def api_fetcher():
    data = access_api(access_token)
    return data

if __name__ == "__main__":
    access_api(access_token)

