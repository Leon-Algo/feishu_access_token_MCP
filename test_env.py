"""
测试环境变量加载和飞书 Token 获取功能
"""

import os
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

# 从环境变量中获取飞书应用凭证
app_id = os.getenv("FEISHU_APP_ID")
app_secret = os.getenv("FEISHU_APP_SECRET")

print(f"App ID: {app_id}")
print(f"App Secret: {app_secret}")

# 测试获取 app_access_token
def test_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") == 0:
            print("Successfully obtained app_access_token:")
            print(f"app_access_token: {data.get('app_access_token')}")
            print(f"expire: {data.get('expire')}")
            return True
        else:
            print(f"Failed to obtain token: {data.get('msg')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Feishu token acquisition...")
    test_feishu_token()