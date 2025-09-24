"""
部署前测试脚本
"""

import os
import sys
from pathlib import Path

def test_directory_structure():
    """测试目录结构"""
    print("测试目录结构...")
    
    # 检查必要的文件和目录
    required_paths = [
        "src",
        "src/feishu_access_token_mcp",
        "src/feishu_access_token_mcp/__init__.py",
        "src/feishu_access_token_mcp/server.py",
        "pyproject.toml",
        "uv.lock",
        "smithery.yaml"
    ]
    
    for path in required_paths:
        if Path(path).exists():
            print(f"✓ {path} 存在")
        else:
            print(f"✗ {path} 不存在")
            return False
    
    return True

def test_module_import():
    """测试模块导入"""
    print("\n测试模块导入...")
    
    try:
        # 添加 src 到 Python 路径
        sys.path.insert(0, "src")
        
        # 尝试导入模块
        from feishu_access_token_mcp.server import create_server
        print("✓ 成功导入 feishu_access_token_mcp.server")
        
        # 尝试创建服务器实例
        server = create_server()
        print(f"✓ 成功创建服务器实例: {server.name}")
        
        return True
    except Exception as e:
        print(f"✗ 导入模块时出错: {e}")
        return False

def test_pyproject_config():
    """测试 pyproject.toml 配置"""
    print("\n测试 pyproject.toml 配置...")
    
    try:
        import toml
        
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            config = toml.load(f)
        
        # 检查必要的配置项
        tool_smithery = config.get("tool", {}).get("smithery", {})
        server_entry = tool_smithery.get("server")
        
        if server_entry == "feishu_access_token_mcp.server:create_server":
            print("✓ Smithery 服务器入口点配置正确")
        else:
            print(f"✗ Smithery 服务器入口点配置不正确: {server_entry}")
            return False
            
        return True
    except Exception as e:
        print(f"✗ 检查 pyproject.toml 时出错: {e}")
        return False

def main():
    """主函数"""
    print("=== 部署前测试 ===")
    
    tests = [
        test_directory_structure,
        test_module_import,
        test_pyproject_config
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n=== 测试结果 ===")
    if all_passed:
        print("✓ 所有测试通过，项目应该可以成功部署到 Smithery")
        return 0
    else:
        print("✗ 部分测试失败，请检查上述错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())