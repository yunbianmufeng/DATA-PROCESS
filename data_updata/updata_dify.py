import json
import requests
from data_transformation.data_enricher import data_enricher
DOCUMENTS_ID = "b29b2b9***b4af29d4267"
GET_DATASETS_documents_LIST_URL = f"http://1***7.244/dify/v1/datasets/{DOCUMENTS_ID}/documents?limit=100"
DATASETS_KEY = "da***C6UVkZn5kWJ"
UPDATE_BY_TEXT_URL = f"http://19***44/dify/v1/datasets/{DOCUMENTS_ID}/documents/"
CREATE_BY_TEXT_URL = f"http://19***244/dify/v1/datasets/{DOCUMENTS_ID}/document/"

def get_doucuments_list():
    headers = {
        "Authorization": f"Bearer {DATASETS_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(GET_DATASETS_documents_LIST_URL, headers=headers)
        response.raise_for_status()

        try:
            data = response.json()
            # print("doucuments_list===>get_doucuments_list=API响应数据：")
            # print(f"doucuments_list===>{data["data"]}")
            return data["data"]

        except ValueError:
            print("响应内容（非JSON格式）：")
            print(response.text)
            return

    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
        return
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')
        return


def find_document_id(doucuments_list, company_name):
    # print("find_document_id(doucuments_list, company_name)")
    for doucument in doucuments_list:

        if doucument["name"] == company_name:
            # print("doucument_id并返回")
            return doucument["id"]


def update_doucument(document_id, company_name, data):
    url = f"{UPDATE_BY_TEXT_URL}{document_id}/update-by-text"
    headers = {
        "Authorization": f"Bearer {DATASETS_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "name": company_name,
        "text": data,
        "indexing_technique": "high_quality",
        "doc_form": "hierarchical_model",
        "process_rule": {
            "mode": "hierarchical",  # hierarchical/custom/automatic
            "rules": {
                "pre_processing_rules": [
                    {
                        "id": "remove_extra_spaces",
                        "enabled": True,
                    },
                    {
                        "id": "remove_urls_emails",
                        "enabled": False,
                    }
                ],
                "segmentation": {
                    "separator": '#',
                    "max_tokens": 1000
                },
                "parent_mode": "paragraph",
                "subchunk_segmentation": {
                    "separator": '\n',
                    "max_tokens": 500,
                    # "chunk_overlap": 50
                }
            }
        },
        "retrieval_model": {
            "search_method": "semantic_search",
            "reranking_enable": False,
            "top_k": 8,
            "score_threshold_enabled": True,
            "score_threshold": 0.20,
            "embedding_model": "bge-m3",
            "embedding_model_provider": "Ollama"
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()

        try:
            datat = response.json()
            print(f"POST结果:{datat}")
        except ValueError:
            print("响应内容（非JSON格式）：")
            print(response.text)
    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("请求成功，响应数据：")
        print(response.text)

    # response = requests.post(url, headers=headers, data=json.dumps(data))
    # if response.status_code == 200:
    #     print("请求成功，响应数据：")
    #     print(response.text)


def create_doucument(company_name, data):
    url = f"{CREATE_BY_TEXT_URL}/create-by-text"
    headers = {
        "Authorization": f"Bearer {DATASETS_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "name": company_name,
        "text": data,
        "indexing_technique": "high_quality",
        "doc_form": "hierarchical_model",
        "process_rule": {
            "mode": "hierarchical",#hierarchical/custom/automatic
            "rules": {
                "pre_processing_rules": [
                    {
                        "id": "remove_extra_spaces",
                        "enabled": True,
                    },
                    {
                        "id": "remove_urls_emails",
                        "enabled": False,
                    }
                ],
                "segmentation": {
                    "separator": '#',
                    "max_tokens": 1000
                },
                "parent_mode": "paragraph",
                "subchunk_segmentation": {
                    "separator": '\n',
                    "max_tokens": 500,
                    # "chunk_overlap": 50
                }
            }
        },
        "retrieval_model": {
            "search_method": "semantic_search",
            "reranking_enable": False,
            "top_k": 8,
            "score_threshold_enabled": True,
            "score_threshold": 0.20,
            "embedding_model": "bge-m3",
            "embedding_model_provider": "Ollama"
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()

        try:
            datat = response.json()
            print(f"POST结果:{datat}")
        except ValueError:
            print("响应内容（非JSON格式）：")
            print(response.text)
    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("请求成功，响应数据：")
        print(response.text)

def updata_dafy(doucuments_list, data):

    company_name = f"{data["name"]}.txt"
    doucument_id = find_document_id(doucuments_list, company_name)
    enricher_data = data_enricher(data)
    if doucument_id is not None:
        print("知识库中已有，执行更新操作")
        update_doucument(doucument_id, company_name, enricher_data)
    else:
        print("知识库中未存在，执行新建操作")
        create_doucument(company_name, enricher_data)
