"""
完整的 MCP 服务测试脚本
"""

import os
import json
from dotenv import load_dotenv
from src.feishu_access_token_mcp.server import create_server

# 加载环境变量
load_dotenv()

class MockContext:
    """模拟 MCP Context"""
    def __init__(self, app_id, app_secret):
        self.session_config = type('SessionConfig', (), {
            'app_id': app_id,
            'app_secret': app_secret
        })()

def test_mcp_server():
    """测试完整的 MCP 服务器功能"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("请确保在 .env 文件中设置了 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        return
    
    print("创建 MCP 服务器实例...")
    server = create_server()
    
    print("测试 get_feishu_token 工具...")
    # 创建模拟上下文
    mock_context = MockContext(app_id, app_secret)
    
    try:
        # 调用 get_feishu_token 工具
        result = None
        for tool in server.tools:
            if tool.name == "get_feishu_token":
                result = tool.fn(mock_context)
                break
        
        if result:
            print("成功获取飞书 Token:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 验证返回的字段
            required_fields = ["app_access_token", "expires_at"]
            for field in required_fields:
                if field in result:
                    print(f"✓ 包含字段: {field}")
                else:
                    print(f"✗ 缺少字段: {field}")
        else:
            print("未找到 get_feishu_token 工具")
            
    except Exception as e:
        print(f"调用工具时出错: {e}")

if __name__ == "__main__":
    print("=== 飞书 Access Token MCP 服务测试 ===")
    test_mcp_server()
    print("=== 测试完成 ===")