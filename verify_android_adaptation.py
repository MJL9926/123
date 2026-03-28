#!/usr/bin/env python3
"""
Android适配验证脚本
检查代码是否完全适配Android平台
"""

import os
import sys
import re
import ast

def check_file_exists(filename):
    """检查文件是否存在"""
    if os.path.exists(filename):
        print(f"✓ {filename} 存在")
        return True
    else:
        print(f"✗ {filename} 不存在")
        return False

def check_python_imports(filename):
    """检查Python导入语句"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查必要的导入
    required_imports = [
        'kivy',
        'requests',
        'pandas',
        'numpy',
        'sklearn'
    ]
    
    print("\n检查Python导入:")
    for imp in required_imports:
        if imp in content:
            print(f"✓ 导入 {imp}")
        else:
            print(f"✗ 缺少导入 {imp}")
            return False
    
    return True

def check_android_adaptation(filename):
    """检查Android适配情况"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n检查Android适配:")
    
    checks = {
        '平台检测': 'from kivy.utils import platform',
        'Android存储路径': 'from android.storage import app_storage_path',
        '平台判断': 'IS_ANDROID',
        '文件路径处理': 'os.path.join',
        '自动交易适配': 'AUTO_TRADE_METHOD',
        '语音播报适配': 'TTS_METHOD'
    }
    
    all_passed = True
    for check_name, check_pattern in checks.items():
        if check_pattern in content:
            print(f"✓ {check_name}")
        else:
            print(f"✗ {check_name} 未找到")
            all_passed = False
    
    return all_passed

def check_file_operations(filename):
    """检查文件操作是否适配Android"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n检查文件操作:")
    
    # 检查是否使用了正确的文件路径处理
    issues = []
    
    # 检查硬编码路径（排除在IS_DESKTOP条件下的路径）
    lines = content.split('\n')
    in_desktop_block = False
    desktop_block_depth = 0
    
    for line in lines:
        # 检查是否进入或退出IS_DESKTOP块
        if 'if IS_DESKTOP:' in line or 'if not IS_ANDROID:' in line:
            in_desktop_block = True
            desktop_block_depth += 1
        elif in_desktop_block and line.strip().startswith('else:'):
            # 跳过else块
            pass
        elif in_desktop_block and line.strip() and not line.strip().startswith('#'):
            # 检查缩进是否减少，表示退出块
            if not line.startswith('    ') and not line.startswith('\t'):
                in_desktop_block = False
                desktop_block_depth = 0
        
        # 只在非桌面平台代码中检查硬编码路径
        if not in_desktop_block:
            hardcoded_paths = re.findall(r'["\']([A-Za-z]:\\[^"\']+)["\']', line)
            if hardcoded_paths:
                print(f"✗ 发现硬编码的Windows路径: {hardcoded_paths}")
                issues.append("硬编码路径")
    
    if not any('硬编码路径' in issue for issue in issues):
        print("✓ 未发现硬编码路径")
    
    # 检查是否使用了os.path.join
    if 'os.path.join' in content:
        print("✓ 使用os.path.join处理路径")
    else:
        print("✗ 未使用os.path.join处理路径")
        issues.append("路径处理")
    
    # 检查异常处理
    if 'try:' in content and 'except' in content:
        print("✓ 文件操作有异常处理")
    else:
        print("✗ 文件操作缺少异常处理")
        issues.append("异常处理")
    
    return len(issues) == 0

def check_network_operations(filename, buildozer_file):
    """检查网络操作是否适配Android"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n检查网络操作:")
    
    # 检查是否使用了requests库
    if 'import requests' in content or 'from requests' in content:
        print("✓ 使用requests库进行网络请求")
    else:
        print("✗ 未使用requests库")
        return False
    
    # 检查buildozer.spec中的网络权限配置
    if os.path.exists(buildozer_file):
        with open(buildozer_file, 'r', encoding='utf-8') as f:
            buildozer_content = f.read()
        
        if 'INTERNET' in buildozer_content:
            print("✓ 配置了INTERNET权限")
        else:
            print("✗ 未配置INTERNET权限")
            return False
    else:
        print("✗ 未找到buildozer.spec文件")
        return False
    
    return True

def check_platform_specific_features(filename):
    """检查平台特定功能"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n检查平台特定功能:")
    
    # 检查自动交易功能
    if 'AUTO_TRADE_METHOD' in content:
        print("✓ 自动交易功能已适配")
    else:
        print("✗ 自动交易功能未适配")
        return False
    
    # 检查语音播报功能
    if 'TTS_METHOD' in content:
        print("✓ 语音播报功能已适配")
    else:
        print("✗ 语音播报功能未适配")
        return False
    
    # 检查字体处理
    if 'msyh' in content or 'Arial' in content:
        print("✓ 字体处理已配置")
    else:
        print("✗ 字体处理未配置")
        return False
    
    return True

def check_buildozer_config(filename):
    """检查buildozer配置"""
    print("\n检查buildozer配置:")
    
    if not os.path.exists(filename):
        print(f"✗ {filename} 不存在")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_configs = {
        'title': 'title =',
        'package.name': 'package.name =',
        'requirements': 'requirements =',
        'android.permissions': 'android.permissions =',
        'android.api': 'android.api =',
        'android.minapi': 'android.minapi ='
    }
    
    all_passed = True
    for config_name, config_pattern in required_configs.items():
        if config_pattern in content:
            print(f"✓ {config_name} 已配置")
        else:
            print(f"✗ {config_name} 未配置")
            all_passed = False
    
    return all_passed

def check_requirements(filename):
    """检查requirements.txt"""
    print("\n检查requirements.txt:")
    
    if not os.path.exists(filename):
        print(f"✗ {filename} 不存在")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_packages = [
        'kivy',
        'requests',
        'pandas',
        'numpy',
        'scikit-learn'
    ]
    
    all_passed = True
    for package in required_packages:
        if package.lower() in content.lower():
            print(f"✓ {package}")
        else:
            print(f"✗ {package} 未列出")
            all_passed = False
    
    return all_passed

def main():
    """主函数"""
    print("=" * 50)
    print("  Android适配验证")
    print("=" * 50)
    
    # 设置文件路径
    project_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(project_dir, 'btc_5min_kivy.py')
    buildozer_file = os.path.join(project_dir, 'buildozer.spec')
    requirements_file = os.path.join(project_dir, 'requirements.txt')
    
    # 检查文件存在性
    print("\n检查文件存在性:")
    file_checks = [
        check_file_exists(main_file),
        check_file_exists(buildozer_file),
        check_file_exists(requirements_file)
    ]
    
    if not all(file_checks):
        print("\n✗ 文件检查失败")
        return False
    
    # 检查Python导入
    if not check_python_imports(main_file):
        print("\n✗ Python导入检查失败")
        return False
    
    # 检查Android适配
    if not check_android_adaptation(main_file):
        print("\n✗ Android适配检查失败")
        return False
    
    # 检查文件操作
    if not check_file_operations(main_file):
        print("\n✗ 文件操作检查失败")
        return False
    
    # 检查网络操作
    if not check_network_operations(main_file, buildozer_file):
        print("\n✗ 网络操作检查失败")
        return False
    
    # 检查平台特定功能
    if not check_platform_specific_features(main_file):
        print("\n✗ 平台特定功能检查失败")
        return False
    
    # 检查buildozer配置
    if not check_buildozer_config(buildozer_file):
        print("\n✗ buildozer配置检查失败")
        return False
    
    # 检查requirements.txt
    if not check_requirements(requirements_file):
        print("\n✗ requirements.txt检查失败")
        return False
    
    print("\n" + "=" * 50)
    print("✓ 所有检查通过！代码已完全适配Android平台")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)