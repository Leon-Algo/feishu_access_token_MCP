"""
测试 MCP 服务的脚本
"""

import requests
import json

# MCP 服务器地址
MCP_SERVER_URL = "http://127.0.0.1:8082/mcp"

def send_mcp_request(method, params=None):
    """发送 MCP 请求"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method
    }
    
    if params:
        payload["params"] = params
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(MCP_SERVER_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def test_initialize():
    """测试 initialize 方法"""
    print("Testing initialize...")
    result = send_mcp_request("initialize", {
        "capabilities": {}
    })
    print(f"Initialize result: {result}")
    return result

def test_list_tools():
    """测试 list_tools 方法"""
    print("Testing list_tools...")
    result = send_mcp_request("tools/list")
    print(f"List tools result: {result}")
    return result

def test_get_feishu_token():
    """测试 get_feishu_token 方法"""
    print("Testing get_feishu_token...")
    # 从环境变量获取凭证
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    result = send_mcp_request("tools/call", {
        "name": "get_feishu_token",
        "arguments": {
            "app_id": os.getenv("FEISHU_APP_ID", ""),
            "app_secret": os.getenv("FEISHU_APP_SECRET", "")
        }
    })
    print(f"Get feishu token result: {result}")
    return result

if __name__ == "__main__":
    print("Testing MCP service...")
    
    # 测试 initialize
    initialize_result = test_initialize()
    
    # 测试 list_tools
    list_tools_result = test_list_tools()
    
    # 测试 get_feishu_token
    get_token_result = test_get_feishu_token()
    
    print("MCP service test completed.")