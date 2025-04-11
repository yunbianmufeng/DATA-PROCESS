import json
import requests
import io
import sys

AUTHING_DOMAIN = "https:***.authing.cn"
ACCESS_KEY = "67e2****278094ee"
SECRET_KEY = "c6e20ee2****1f81a74e2"
TOKEN_ENDPOINT = f"{AUTHING_DOMAIN}/oidc/token"
SUMMARY_API_ENDPOINT = "http://4****/invest/projects/_summary"
TAX_API_ENDPOINT = "http://47.1*****52/api/invest/projects/_summary_revenue_tax"
FINANCIAL_API_ENDPOINT = "http://47*****152/api/invest/projects/_summary_financial"

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


def summary_data_enricher(data):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    print("#山东产业技术研究院（青岛）生态平台绩效:")
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

if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        summary_api_data = access_api(access_token,SUMMARY_API_ENDPOINT)
        tax_api_data = access_api(access_token,TAX_API_ENDPOINT)
        financial_api_data = access_api(access_token,FINANCIAL_API_ENDPOINT)
        if summary_api_data:
            print("获取到的 API 数据:")
            print(summary_api_data)
            print(summary_data_enricher(summary_api_data))
        if tax_api_data:
            print("获取到的 API 数据:")
            print(tax_api_data)
            print(tax_data_enricher(tax_api_data))
        if financial_api_data:
            print("获取到的 API 数据:")
            print(financial_api_data)
            print(financial_data_enricher(financial_api_data))

else:
    print("获取 AccessToken 失败")
