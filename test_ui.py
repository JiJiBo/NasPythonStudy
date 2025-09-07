#!/usr/bin/env python3
"""
UI界面测试脚本
用于验证本地模型管理界面是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ui_components():
    """测试UI组件是否能正常导入和创建"""
    print("=" * 50)
    print("测试UI组件")
    print("=" * 50)
    
    try:
        # 测试LocalModelManager导入
        print("1. 测试LocalModelManager导入...")
        from src.utils.LocalModelManager import local_model_manager
        print("   ✓ LocalModelManager导入成功")
        
        # 测试模型管理器基本功能
        print("\n2. 测试模型管理器基本功能...")
        available_models = local_model_manager.get_available_models()
        print(f"   ✓ 获取到 {len(available_models)} 个可用模型")
        
        installed_models = local_model_manager.get_installed_models()
        print(f"   ✓ 获取到 {len(installed_models)} 个已安装模型")
        
        status = local_model_manager.get_model_status()
        print(f"   ✓ 模型状态: {status['current_model']}")
        
        # 测试Flet组件创建
        print("\n3. 测试Flet组件创建...")
        import flet as ft
        
        # 创建基本组件
        dropdown = ft.Dropdown(
            label="测试下拉框",
            options=[
                ft.dropdown.Option("test1"),
                ft.dropdown.Option("test2"),
            ]
        )
        print("   ✓ Dropdown组件创建成功")
        
        button = ft.ElevatedButton("测试按钮")
        print("   ✓ Button组件创建成功")
        
        container = ft.Container(
            content=ft.Column([dropdown, button]),
            visible=True
        )
        print("   ✓ Container组件创建成功")
        
        # 测试本地模型管理界面组件
        print("\n4. 测试本地模型管理界面组件...")
        
        # 创建模型列表项
        model_list = []
        for model_name, model_info in available_models.items():
            size_mb = model_info.size // (1024 * 1024)
            
            list_tile = ft.ListTile(
                leading=ft.Icon(ft.Icons.MEMORY, size=24),
                title=ft.Text(model_name, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{size_mb}MB - {model_info.description}", 
                               size=12, color=ft.Colors.GREY),
                trailing=ft.Row([
                    ft.ElevatedButton("下载"),
                    ft.IconButton(ft.Icons.DELETE, tooltip="删除模型")
                ], spacing=5),
                content_padding=ft.Padding(5, 5, 5, 5)
            )
            model_list.append(list_tile)
        
        print(f"   ✓ 创建了 {len(model_list)} 个模型列表项")
        
        # 创建对话框内容
        dialog_content = ft.Container(
            content=ft.Column([
                ft.Text("本地模型管理", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Column(model_list, scroll=ft.ScrollMode.AUTO)
            ]),
            padding=20,
            width=600,
            height=500
        )
        print("   ✓ 对话框内容创建成功")
        
        print("\n✓ 所有UI组件测试通过")
        return True
        
    except Exception as e:
        print(f"✗ UI组件测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_settings_import():
    """测试LLM设置页面导入"""
    print("\n" + "=" * 50)
    print("测试LLM设置页面导入")
    print("=" * 50)
    
    try:
        # 测试导入LLM设置页面
        print("1. 测试导入LLM设置页面...")
        from src.ui.llm.llm_settings import llm_setting_page
        print("   ✓ LLM设置页面导入成功")
        
        # 测试导入设置内容页面
        print("2. 测试导入设置内容页面...")
        from src.ui.home.setting_content import SettingContent
        print("   ✓ 设置内容页面导入成功")
        
        print("\n✓ LLM设置页面导入测试通过")
        return True
        
    except Exception as e:
        print(f"✗ LLM设置页面导入测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("UI界面功能测试")
    print("=" * 60)
    
    tests = [
        ("UI组件创建", test_ui_components),
        ("LLM设置页面导入", test_llm_settings_import),
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
        print("\n🎉 所有UI测试通过！界面组件正常工作。")
        print("\n下一步:")
        print("1. 启动应用: python main.py")
        print("2. 进入设置页面测试本地模型管理功能")
        print("3. 检查界面是否正常显示")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查相关功能。")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
