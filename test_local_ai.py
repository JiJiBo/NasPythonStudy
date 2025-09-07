#!/usr/bin/env python3
"""
本地AI模型功能测试脚本
用于验证LocalModelManager和UpdateManager的功能
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_local_model_manager():
    """测试本地模型管理器"""
    print("=" * 50)
    print("测试本地模型管理器")
    print("=" * 50)
    
    try:
        from src.utils.LocalModelManager import local_model_manager
        
        # 测试获取可用模型
        print("1. 获取可用模型列表...")
        available_models = local_model_manager.get_available_models()
        print(f"   找到 {len(available_models)} 个可用模型:")
        for name, info in available_models.items():
            size_mb = info.size // (1024 * 1024)
            print(f"   - {name}: {size_mb}MB - {info.description}")
        
        # 测试获取已安装模型
        print("\n2. 检查已安装模型...")
        installed_models = local_model_manager.get_installed_models()
        print(f"   已安装 {len(installed_models)} 个模型:")
        for model in installed_models:
            print(f"   - {model.name}")
        
        # 测试模型状态
        print("\n3. 获取模型状态...")
        status = local_model_manager.get_model_status()
        print(f"   当前模型: {status['current_model']}")
        print(f"   是否已加载: {status['is_loaded']}")
        print(f"   已安装模型: {status['installed_models']}")
        
        # 如果有已安装的模型，尝试加载
        if installed_models:
            print("\n4. 测试模型加载...")
            first_model = installed_models[0]
            print(f"   尝试加载模型: {first_model.name}")
            
            if local_model_manager.load_model(first_model.name):
                print("   ✓ 模型加载成功")
                
                # 测试简单推理
                print("\n5. 测试模型推理...")
                test_prompt = "请解释什么是Python中的列表推导式"
                print(f"   测试提示: {test_prompt}")
                
                response = local_model_manager.get_response(test_prompt, max_tokens=200)
                print(f"   模型响应: {response[:200]}...")
                
            else:
                print("   ✗ 模型加载失败")
        else:
            print("\n4. 没有已安装的模型，跳过加载测试")
            print("   提示: 可以通过应用界面下载模型")
        
        print("\n✓ 本地模型管理器测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 本地模型管理器测试失败: {str(e)}")
        return False

def test_update_manager():
    """测试更新管理器"""
    print("\n" + "=" * 50)
    print("测试更新管理器")
    print("=" * 50)
    
    try:
        from src.utils.UpdateManager import update_manager
        
        # 测试获取更新状态
        print("1. 检查更新状态...")
        update_status = update_manager.get_update_status()
        
        app_update = update_status.get("app_update")
        if app_update:
            if app_update.get("has_update"):
                print(f"   发现应用更新: {app_update['current_version']} -> {app_update['remote_version']}")
            else:
                print("   应用已是最新版本")
        else:
            print("   无法检查应用更新（可能是网络问题或配置问题）")
        
        model_updates = update_status.get("model_updates", {})
        if model_updates:
            print(f"   检查了 {len(model_updates)} 个模型的更新状态")
            for model_name, update_info in model_updates.items():
                if update_info.get("has_update"):
                    print(f"   - {model_name}: 有更新")
                else:
                    print(f"   - {model_name}: 已是最新")
        else:
            print("   没有检查到模型更新信息")
        
        print("\n✓ 更新管理器测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 更新管理器测试失败: {str(e)}")
        return False

def test_chat_integration():
    """测试聊天集成"""
    print("\n" + "=" * 50)
    print("测试聊天集成")
    print("=" * 50)
    
    try:
        from src.utils.ChatUtils import AIRequestHandlerWithHistory
        from src.db.llm_config_db import LLMConfigDB
        
        # 检查是否有本地模型配置
        db = LLMConfigDB()
        local_configs = db.get_configs_by_provider("local")
        
        if local_configs:
            print("1. 找到本地模型配置")
            for config in local_configs:
                print(f"   - 模型: {config.get('model')}")
            
            # 测试聊天处理器
            print("\n2. 测试聊天处理器...")
            chat_handler = AIRequestHandlerWithHistory()
            
            # 检查处理器是否有效
            if chat_handler.handler.valid:
                print("   ✓ 聊天处理器初始化成功")
                
                # 测试单次响应（如果有已加载的模型）
                from src.utils.LocalModelManager import local_model_manager
                if local_model_manager.current_model:
                    print("\n3. 测试单次响应...")
                    test_prompt = "什么是Python的装饰器？"
                    print(f"   测试提示: {test_prompt}")
                    
                    chat_id, response = chat_handler.get_single_response("test_chat", test_prompt)
                    if response:
                        print(f"   响应长度: {len(response)} 字符")
                        print(f"   响应预览: {response[:100]}...")
                    else:
                        print("   没有收到响应")
                else:
                    print("\n3. 没有加载的模型，跳过响应测试")
            else:
                print("   ✗ 聊天处理器初始化失败")
        else:
            print("1. 没有找到本地模型配置")
            print("   提示: 请先在应用中配置本地模型")
        
        print("\n✓ 聊天集成测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 聊天集成测试失败: {str(e)}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n" + "=" * 50)
    print("测试文件结构")
    print("=" * 50)
    
    required_files = [
        "src/utils/LocalModelManager.py",
        "src/utils/UpdateManager.py", 
        "src/utils/ChatUtils.py",
        "src/ui/llm/llm_settings.py",
        "src/ui/home/setting_content.py",
        "pyproject.toml",
        "AI_辅助Python学习应用完整方案.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} (缺失)")
            missing_files.append(file_path)
    
    # 检查models目录
    models_dir = Path("models")
    if models_dir.exists():
        print(f"   ✓ models/ 目录存在")
        model_files = list(models_dir.glob("*.gguf"))
        print(f"   - 找到 {len(model_files)} 个模型文件")
    else:
        print(f"   ! models/ 目录不存在（将在首次下载模型时创建）")
    
    if missing_files:
        print(f"\n✗ 发现 {len(missing_files)} 个缺失文件")
        return False
    else:
        print(f"\n✓ 所有必需文件都存在")
        return True

def main():
    """主测试函数"""
    print("AI 辅助 Python 学习应用 - 功能测试")
    print("=" * 60)
    
    # 检查Python版本
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print()
    
    # 运行测试
    tests = [
        ("文件结构", test_file_structure),
        ("本地模型管理器", test_local_model_manager),
        ("更新管理器", test_update_manager),
        ("聊天集成", test_chat_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {str(e)}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("\n🎉 所有测试通过！应用已准备就绪。")
        print("\n下一步:")
        print("1. 运行 'python main.py' 启动应用")
        print("2. 进入设置页面配置本地模型")
        print("3. 下载并加载模型开始使用")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查相关功能。")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
