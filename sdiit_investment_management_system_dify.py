import json
import requests
import io
import sys

AUTHING_DOMAIN = "https://sdiitqd-irms.authing.cn"
ACCESS_KEY = "67e***8094ee"
SECRET_KEY = "c6e20***74e2"
TOKEN_ENDPOINT = f"{AUTHING_DOMAIN}/oidc/token"
API_ENDPOINT = "http://47.10***est/projects/_full"
SUMMARY_API_ENDPOINT = "http://47.1****i/invest/projects/_summary"
TAX_API_ENDPOINT = "http://47.104****est/projects/_summary_revenue_tax"
FINANCIAL_API_ENDPOINT = "http://47.***api/invest/projects/_summary_financial"

DOCUMENTS_ID = "34ae76e8-8d0f-41fc-9ee0-ad5c411ae4ce"
GET_DATASETS_documents_LIST_URL = f"http://19**244/dify/v1/datasets/{DOCUMENTS_ID}/documents?limit=100"
DATASETS_KEY = "dataset-9utHq6lNSnKaPC6UVkZn5kWJ"
UPDATE_BY_TEXT_URL = f"http://192.**44/dify/v1/datasets/{DOCUMENTS_ID}/documents/"
CREATE_BY_TEXT_URL = f"http://192.16**.244/dify/v1/datasets/{DOCUMENTS_ID}/document/"


def get_access_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": ACCESS_KEY,
        "client_secret": SECRET_KEY,
        "scope": 'openid roles'
    }

    try:
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except requests.RequestException as e:
        print(f"请求 AccessToken 出错: {e}")
    except ValueError as e:
        print(f"解析 AccessToken 响应出错: {e}")
    return None


def access_api(access_token,url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    # print(headers)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        try:
            data = response.json()
            print("API响应数据：")
            # print(data)
            return data
        except ValueError:
            print("响应内容（非JSON格式）：")
            print(response.text)

    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')

def all_access_api(access_token,url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    # print(headers)
    params = {
        'regi_area': 'ALL'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        try:
            data = response.json()
            # print("API响应数据：")
            # print(data)
            return data
        except ValueError:
            print("响应内容（非JSON格式）：")
            print(response.text)

    except requests.exceptions.HTTPError as err:
        print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{str(e)}')

def data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#企业名称：", data["name"])

    company = data["company"]
    print("#" + data["name"] + "基本信息：")
    if "start_date" in company:
        print("  注册时间：", company["start_date"])
    if "invest_date" in company:
        print("  投资时间：", company["invest_date"])
    print(f"#{data["name"]}基本信息：")
    if "scope" in company:
        print("  主营业务：", company["scope"])
    if "address" in company:
        print("  注册地址：", company["address"])

    capital = data["capital"]
    print(f"#{data["name"]}资本结构：")
    print("  股权结构：")
    if "partners" in capital:
        i = 0
        for partner in capital["partners"]:
            i += 1
            if i <= 6:
                print(f"    投资人：{partner['stock_name']}，股权占比：{partner['stock_percent']}%")
            if i > 6:
                i = 0
                print(f"#{data["name"]}资本结构：")
                print("  股权结构还有：")
                print(f"    投资人：{partner['stock_name']}，股权占比：{partner['stock_percent']}%")

    print("  董监高情况：")
    if "employees" in capital:
        i = 0
        for employee in capital["employees"]:
            i += 1
            if i <= 6:
                print(f"    职位：{employee['job']}，姓名：{employee['name']}")
            if i > 6:
                i = 0
                print(f"#{data["name"]}资本结构：")
                print("  董监高情况还有：")
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
            i = 0
            for ip in intellectual_properties:
                i += 1
                if i <= 6 :
                    print(f"  编号：{ip['no']}")
                    print(f"  名称：{ip['name']}")
                    print(f"  类别：{ip['ip_type']}")
                    print(f"  获得时间：{ip['publish_date']}")
                if i > 6:
                    i = 0
                    print(f"#{data["name"]}创新成果还有：")
                    print(f"  编号：{ip['no']}")
                    print(f"  名称：{ip['name']}")
                    print(f"  类别：{ip['ip_type']}")
                    print(f"  获得时间：{ip['publish_date']}")

    sys.stdout = old_stdout
    data1 = buffer.getvalue()
    buffer.close()
    return data1

def summary_data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#山东产业技术研究院（青岛）生态平台绩效:")
    print(f"山东产业技术研究院（产研院）投资的项目（企业）总数：{data["count"]}")
    print(f"山东产业技术研究院（产研院）的高企数量：{data["count_01"]}")
    print(f"山东产业技术研究院（产研院）的专精特新企业数量：{data["count_02"]}")
    print(f"山东产业技术研究院（产研院）的小巨人企业数量：{data["count_03"]}")
    print(f"山东产业技术研究院（产研院）的瞪羚企业数量：{data["count_04"]}")
    print(f"山东产业技术研究院（产研院）撬动社会资本:企业融资额{data["total_history_actual_financing"]}万元")
    print(f"山东产业技术研究院（产研院）转移转化技术{data["tech_commercialization_count"]}项")

    print("#山东产业技术研究院（青岛）生态创新绩效:")
    print(f"山东产业技术研究院（产研院）人才情况：员工数量：{data["employee_count"]}人")
    print(f"山东产业技术研究院（产研院）人才情况：其中：本科{data["bachelor_count"]}人")
    print(f"山东产业技术研究院（产研院）人才情况：其中：硕士{data["master_count"]}人")
    print(f"山东产业技术研究院（产研院）人才情况：其中：博士{data["doctor_count"]}人")
    print(f"山东产业技术研究院（产研院）荣誉资质：共{data["award_count"]}项")
    print(f"山东产业技术研究院（产研院）知识产权：共{data["ip_count"]}件")
    print(f"山东产业技术研究院（产研院）专利数量：共{data["ip_pt_count"]}件")
    print(f"山东产业技术研究院（产研院）著作权数量：共{data["ip_cr_count"]}件")
    print(f"山东产业技术研究院（产研院）注册商标数量：共{data["ip_tm_count"]}件")

    sys.stdout = old_stdout
    data1 = buffer.getvalue()
    buffer.close()
    return data1

def tax_data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#山东产业技术研究院（青岛）投资项目的利税统计")
    for i in data:
        print(f"山东产业技术研究院（产研院）生态平台绩效：年营业收入:年份：{i["year"]}")
        print(f"山东产业技术研究院（产研院）生态平台绩效：年营业收入:季度：{i["quarter"]}")
        print(f"山东产业技术研究院（产研院）生态平台绩效：年营业收入:营业额：{i["revenue"]}万元")
        print(f"山东产业技术研究院（产研院）生态平台绩效：年营业收入:利润：{i["profit"]}万元")
        print(f"山东产业技术研究院（产研院）生态平台绩效：年营业收入:税：{i["tax"]}万元")

    sys.stdout = old_stdout
    data1 = buffer.getvalue()
    buffer.close()
    return data1

def financial_data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#山东产业技术研究院（青岛）投资项目的资产情况统计:")
    for i in data:
        print(f"山东产业技术研究院（产研院）的资产情况：年份：{i["year"]}年")
        print(f"山东产业技术研究院（产研院）的资产情况：总资产：{i["asset"]}万元")
        print(f"山东产业技术研究院（产研院）的资产情况：总负债：{i["debt"]}万元")
        print(f"山东产业技术研究院（产研院）的资产情况：所有者权益：{i["equity"]}万元")

    sys.stdout = old_stdout
    data1 = buffer.getvalue()
    buffer.close()
    return data1

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
            print("doucuments_list===>get_doucuments_list=API响应数据：")
            print(f"doucuments_list===>{data["data"]}")
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


if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        api_data = access_api(access_token,API_ENDPOINT)
        doucuments_list = get_doucuments_list()
        if api_data:
            print("获取到的 API 数据:")
            i = 1
            # doucuments_list = get_doucuments_list()
            # if doucuments_list is None:
            for data in api_data:
                print('第', i, '家:')
                i += 1
                company_name = f"{data["name"]}.txt"
                print(company_name)
                doucument_id = find_document_id(doucuments_list, company_name)
                data2 = data_enricher(data)
                # print(data2)
                if doucument_id is not None:
                    print("知识库中已有，执行更新操作")
                    update_doucument(doucument_id, company_name, data2)
                else:
                    print("知识库中未存在，执行新建操作")
                    create_doucument(company_name, data2)
        summary_api_data = all_access_api(access_token, SUMMARY_API_ENDPOINT)
        tax_api_data = all_access_api(access_token, TAX_API_ENDPOINT)
        financial_api_data = all_access_api(access_token, FINANCIAL_API_ENDPOINT)
        if summary_api_data:
            name = "山东产业技术研究院（青岛）投资项目汇总信息"
            doucument_id = find_document_id(doucuments_list, name)
            # print(summary_data_enricher(summary_api_data))
            if doucument_id is not None:
                print("知识库中已有，执行更新操作")
                update_doucument(doucument_id, name, summary_data_enricher(summary_api_data))
            else:
                print("知识库中未存在，执行新建操作")
                create_doucument(name, summary_data_enricher(summary_api_data))

        if tax_api_data:
            name = "山东产业技术研究院（青岛）投资项目的利税统计"
            doucument_id = find_document_id(doucuments_list, name)
            # print(tax_data_enricher(tax_api_data))
            if doucument_id is not None:
                print("知识库中已有，执行更新操作")
                update_doucument(doucument_id, name, tax_data_enricher(tax_api_data))
            else:
                print("知识库中未存在，执行新建操作")
                create_doucument(name, tax_data_enricher(tax_api_data))
        if financial_api_data:
            name = "山东产业技术研究院（青岛）投资项目资产情况统计"
            doucument_id = find_document_id(doucuments_list, name)
            # print(financial_data_enricher(financial_api_data))
            if doucument_id is not None:
                print("知识库中已有，执行更新操作")
                update_doucument(doucument_id, name, financial_data_enricher(financial_api_data))
            else:
                print("知识库中未存在，执行新建操作")
                create_doucument(name, financial_data_enricher(financial_api_data))
else:
    print("获取 AccessToken 失败")
