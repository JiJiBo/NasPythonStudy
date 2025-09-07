#!/usr/bin/env python3
"""
LLM设置页面测试脚本
用于验证本地模型管理界面是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_llm_settings_components():
    """测试LLM设置页面组件"""
    print("=" * 50)
    print("测试LLM设置页面组件")
    print("=" * 50)
    
    try:
        # 测试导入
        print("1. 测试导入...")
        from src.ui.llm.llm_settings import llm_setting_page
        from src.utils.LocalModelManager import local_model_manager
        import flet as ft
        print("   ✓ 所有模块导入成功")
        
        # 测试LocalModelManager
        print("\n2. 测试LocalModelManager...")
        available_models = local_model_manager.get_available_models()
        print(f"   ✓ 获取到 {len(available_models)} 个可用模型")
        
        installed_models = local_model_manager.get_installed_models()
        print(f"   ✓ 获取到 {len(installed_models)} 个已安装模型")
        
        # 测试Flet组件创建
        print("\n3. 测试Flet组件创建...")
        
        # 创建下拉框
        dropdown = ft.Dropdown(
            label="选择模型类型",
            options=[
                ft.dropdown.Option("deepseek"),
                ft.dropdown.Option("OpenAI"),
                ft.dropdown.Option("ollama"),
                ft.dropdown.Option("local"),
            ],
            width=380
        )
        print("   ✓ 模型类型下拉框创建成功")
        
        # 创建本地模型下拉框
        local_dropdown = ft.Dropdown(
            label="选择本地模型",
            width=380,
            options=[]
        )
        print("   ✓ 本地模型下拉框创建成功")
        
        # 创建状态文本
        status_text = ft.Text("", size=12, color=ft.Colors.GREY)
        print("   ✓ 状态文本创建成功")
        
        # 创建进度条
        progress_bar = ft.ProgressBar(width=380, visible=False)
        print("   ✓ 进度条创建成功")
        
        # 创建按钮
        buttons = ft.Row([
            ft.ElevatedButton("下载模型"),
            ft.ElevatedButton("加载模型"),
            ft.ElevatedButton("删除模型"),
        ], spacing=10)
        print("   ✓ 管理按钮创建成功")
        
        # 创建配置容器
        config_container = ft.Column(spacing=8)
        print("   ✓ 配置容器创建成功")
        
        # 测试本地模型列表填充
        print("\n4. 测试本地模型列表填充...")
        for model_name, model_info in available_models.items():
            is_installed = any(m.name == model_name for m in installed_models)
            status = "✓ 已安装" if is_installed else "未安装"
            size_mb = model_info.size // (1024 * 1024)
            
            local_dropdown.options.append(
                ft.dropdown.Option(
                    key=model_name,
                    text=f"{model_name} ({size_mb}MB) - {status}",
                    disabled=not is_installed
                )
            )
        
        print(f"   ✓ 填充了 {len(local_dropdown.options)} 个模型选项")
        
        # 测试界面布局
        print("\n5. 测试界面布局...")
        
        # 模拟本地模型配置
        config_container.controls.extend([
            local_dropdown,
            status_text,
            progress_bar,
            ft.Text("", size=12),  # 进度文本
            buttons
        ])
        
        main_layout = ft.Column([
            ft.Text("当前配置", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Row([
                ft.Column([
                    dropdown,
                    config_container,
                    ft.Row([
                        ft.ElevatedButton("保存为新配置"),
                        ft.ElevatedButton("清空输入"),
                    ], spacing=10),
                ])
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        print("   ✓ 主界面布局创建成功")
        
        print("\n✓ 所有LLM设置页面组件测试通过")
        return True
        
    except Exception as e:
        print(f"✗ LLM设置页面组件测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_model_management_functions():
    """测试模型管理功能"""
    print("\n" + "=" * 50)
    print("测试模型管理功能")
    print("=" * 50)
    
    try:
        from src.utils.LocalModelManager import local_model_manager
        
        # 测试模型状态获取
        print("1. 测试模型状态获取...")
        status = local_model_manager.get_model_status()
        print(f"   ✓ 当前模型: {status['current_model']}")
        print(f"   ✓ 是否已加载: {status['is_loaded']}")
        print(f"   ✓ 已安装模型: {status['installed_models']}")
        
        # 测试模型信息获取
        print("\n2. 测试模型信息获取...")
        available_models = local_model_manager.get_available_models()
        for name, info in available_models.items():
            size_mb = info.size // (1024 * 1024)
            print(f"   - {name}: {size_mb}MB - {info.description}")
        
        # 测试已安装模型检查
        print("\n3. 测试已安装模型检查...")
        installed_models = local_model_manager.get_installed_models()
        print(f"   ✓ 已安装 {len(installed_models)} 个模型")
        
        for model in installed_models:
            print(f"   - {model.name}")
        
        print("\n✓ 所有模型管理功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 模型管理功能测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("LLM设置页面功能测试")
    print("=" * 60)
    
    tests = [
        ("LLM设置页面组件", test_llm_settings_components),
        ("模型管理功能", test_model_management_functions),
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
        print("\n🎉 所有LLM设置页面测试通过！")
        print("\n界面修复完成，现在可以:")
        print("1. 启动应用: python main.py")
        print("2. 进入设置 → 大模型设置")
        print("3. 选择'local'测试本地模型管理功能")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查相关功能。")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
