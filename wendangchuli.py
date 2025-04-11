import requests

url = "http://192****203/dify/v1/datasets/34ae76e8-8d0f-41fc-9ee0-ad5c411ae4ce/documents?limit=100"
api_key = "dataset-9utHq6lNSnKaPC6UVkZn5kWJ"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # 尝试解析JSON数据
    try:
        data = response.json()
        print("API响应数据：")
        # print(data)
        for i in data["data"]:
            if i["name"] == "青岛谛声声学科技有限公司.txt":
                print(i)

    except ValueError:
        print("响应内容（非JSON格式）：")
        print(response.text)

except requests.exceptions.HTTPError as err:
    print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
except requests.exceptions.RequestException as e:
    print(f'请求异常：{str(e)}')
