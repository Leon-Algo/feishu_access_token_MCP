"""
测试模块导入
"""

try:
    from src.feishu_access_token_mcp.server import create_server
    print("成功导入模块")
    server = create_server()
    print("成功创建服务器实例")
    print(f"服务器名称: {server.name}")
except Exception as e:
    print(f"导入模块时出错: {e}")
    import traceback
    traceback.print_exc()