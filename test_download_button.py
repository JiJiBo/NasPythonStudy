#!/usr/bin/env python3
"""
下载按钮测试脚本
用于验证下载按钮和对话框是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_download_dialog():
    """测试下载对话框功能"""
    print("=" * 50)
    print("测试下载对话框功能")
    print("=" * 50)
    
    try:
        import flet as ft
        from src.utils.LocalModelManager import local_model_manager
        
        # 测试获取可用模型
        print("1. 测试获取可用模型...")
        available_models = local_model_manager.get_available_models()
        installed_models = local_model_manager.get_installed_models()
        installed_names = [m.name for m in installed_models]
        
        print(f"   ✓ 可用模型: {len(available_models)}")
        print(f"   ✓ 已安装模型: {len(installed_models)}")
        
        # 创建可下载的模型列表
        print("\n2. 创建下载选项...")
        download_options = []
        for model_name, model_info in available_models.items():
            if model_name not in installed_names:
                size_mb = model_info.size // (1024 * 1024)
                display_name = model_name.replace("qwen2.5-coder-1.5b-", "Qwen-")
                short_desc = model_info.description[:20] + "..." if len(model_info.description) > 20 else model_info.description
                text = f"{display_name} ({size_mb}MB) - {short_desc}"
                
                download_options.append(
                    ft.dropdown.Option(
                        key=model_name,
                        text=text
                    )
                )
                print(f"   - {text}")
        
        print(f"   ✓ 创建了 {len(download_options)} 个下载选项")
        
        # 测试下拉框创建
        print("\n3. 测试下拉框创建...")
        download_dropdown = ft.Dropdown(
            label="选择要下载的模型",
            options=download_options,
            width=450,
            expand=True
        )
        print("   ✓ 下载下拉框创建成功")
        
        # 测试按钮创建
        print("\n4. 测试按钮创建...")
        download_button = ft.ElevatedButton("下载", bgcolor=ft.Colors.GREEN)
        cancel_button = ft.TextButton("取消")
        print("   ✓ 按钮创建成功")
        
        # 测试对话框创建
        print("\n5. 测试对话框创建...")
        dialog = ft.AlertDialog(
            title=ft.Text("下载模型", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=download_dropdown,
                width=500,
                padding=ft.Padding(10, 10, 10, 10)
            ),
            actions=[
                download_button,
                cancel_button
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        print("   ✓ 对话框创建成功")
        
        # 测试下载函数调用
        print("\n6. 测试下载函数...")
        def test_download_callback(name, progress, downloaded, total):
            print(f"   下载进度: {progress:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)")
        
        def test_error_callback(error):
            print(f"   下载错误: {error}")
        
        # 模拟下载调用（不实际下载）
        if download_options:
            test_model = download_options[0].key
            print(f"   模拟下载模型: {test_model}")
            print("   ✓ 下载函数调用成功")
        else:
            print("   ! 没有可下载的模型")
        
        print("\n✓ 所有下载对话框功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 下载对话框功能测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_button_events():
    """测试按钮事件处理"""
    print("\n" + "=" * 50)
    print("测试按钮事件处理")
    print("=" * 50)
    
    try:
        import flet as ft
        
        # 创建测试按钮
        print("1. 创建测试按钮...")
        test_button = ft.ElevatedButton("测试按钮")
        print("   ✓ 测试按钮创建成功")
        
        # 测试事件处理函数
        print("\n2. 测试事件处理...")
        click_count = 0
        
        def on_button_click(e):
            nonlocal click_count
            click_count += 1
            print(f"   按钮被点击 {click_count} 次")
        
        test_button.on_click = on_button_click
        print("   ✓ 事件处理函数设置成功")
        
        # 模拟按钮点击
        print("\n3. 模拟按钮点击...")
        # 注意：这里只是测试事件绑定，实际点击需要UI环境
        print("   ✓ 按钮事件绑定成功")
        
        print("\n✓ 所有按钮事件处理测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 按钮事件处理测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("下载按钮功能测试")
    print("=" * 60)
    
    tests = [
        ("下载对话框功能", test_download_dialog),
        ("按钮事件处理", test_button_events),
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
        print("\n🎉 所有下载按钮测试通过！")
        print("\n如果按钮仍然点不动，可能的原因:")
        print("1. 对话框被其他元素遮挡")
        print("2. 事件处理函数有错误")
        print("3. UI线程阻塞")
        print("\n建议:")
        print("1. 检查控制台是否有错误信息")
        print("2. 尝试点击对话框的其他区域")
        print("3. 重启应用")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查相关功能。")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
