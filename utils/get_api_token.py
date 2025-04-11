import requests

AUTHING_DOMAIN = "https://s****s.authing.cn"
ACCESS_KEY = "67e****78094ee"
SECRET_KEY = "c6e20ee*****61f81a74e2"
TOKEN_ENDPOINT = f"{AUTHING_DOMAIN}/oidc/token"

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