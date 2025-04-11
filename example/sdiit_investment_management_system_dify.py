from utils.get_api_token import get_access_token
from data_collection.api_fetcher import access_api
from data_cleaning.null_handler import handle_null_values_forjson
from data_updata.updata_dify import get_doucuments_list
from data_updata.updata_dify import updata_dafy
if __name__ == '__main__':
    access_token = get_access_token()#获取HTTP请求服务器数据库的token
    if access_token is not None:
        API_ENDPOINT = "http://47.***.152/api/invest/projects/_full"
        api_data = access_api(API_ENDPOINT, access_token)#服务器返回HTTP请求的Json数据
        data = handle_null_values_forjson(api_data)#数据清洗-去除无用的空值数据
        i = 1 #记录处理的document数
        doucuments_list = get_doucuments_list()#获取DIfy知识库中的文档列表
        for data in data:
            print('第',i ,'家：')
            i += 1
            updata_dafy(doucuments_list, data)