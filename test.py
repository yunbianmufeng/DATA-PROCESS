import requests
import json
def main(txt: str,name:str) -> dict:

    url = "http://192.****95-a49865bdb8c6/document/create-by-text"
    api_key = "dataset-kTtY7iy6DNoIluNRvZ45c15V"  # 请替换为您的实际API密钥

    # 定义请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 定义请求数据
    data = {
        "name": name,
        "text": txt,
        "indexing_technique": "high_quality",
        "process_rule": {
            "mode": "automatic"
        }
    }
    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 检查响应并打印结果
    if response.status_code == 200:
        print("请求成功，响应数据：")

    return {
        "result": response.status_code,
    }