"""
简单的飞书 Token 获取测试
"""

import os
from dotenv import load_dotenv
from src.feishu_access_token_mcp.server import create_server

# 加载环境变量
load_dotenv()

def test_token_manager():
    """测试 TokenManager"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("请确保在 .env 文件中设置了 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        return
    
    # 创建服务器实例
    server = create_server()
    
    # 注意：这里我们需要模拟一个完整的 MCP 上下文来测试
    # 由于直接测试比较复杂，我们直接测试 TokenManager
    from src.feishu_access_token_mcp.server import FeishuTokenManager
    
    # 创建 TokenManager 实例
    token_manager = FeishuTokenManager(app_id, app_secret)
    
    # 获取 Token 信息
    token_info, error = token_manager.get_token_info()
    
    if error:
        print(f"获取 Token 失败: {error}")
    else:
        print("成功获取 Token 信息:")
        print(f"app_access_token: {token_info.get('app_access_token')}")
        print(f"expires_at: {token_info.get('expires_at')}")

if __name__ == "__main__":
    print("测试飞书 Token 获取...")
    test_token_manager()