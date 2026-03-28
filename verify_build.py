#!/usr/bin/env python3
"""
APK构建验证脚本
检查APK文件是否已成功构建
"""

import os
import sys

def check_apk_files():
    """检查APK文件是否存在"""
    print("=" * 50)
    print("  APK构建验证")
    print("=" * 50)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(project_dir, "bin")
    
    print(f"\n项目目录: {project_dir}")
    print(f"bin目录: {bin_dir}")
    
    # 检查bin目录是否存在
    if not os.path.exists(bin_dir):
        print("\n✗ bin目录不存在")
        print("\nAPK文件尚未构建")
        return False
    
    print("\n✓ bin目录存在")
    
    # 查找APK文件
    apk_files = []
    for file in os.listdir(bin_dir):
        if file.endswith('.apk'):
            apk_files.append(os.path.join(bin_dir, file))
    
    if not apk_files:
        print("\n✗ 未找到APK文件")
        print("\nAPK文件尚未构建")
        return False
    
    print(f"\n✓ 找到 {len(apk_files)} 个APK文件:")
    
    for apk in apk_files:
        size = os.path.getsize(apk)
        size_mb = size / (1024 * 1024)
        print(f"  - {os.path.basename(apk)} ({size_mb:.1f} MB)")
    
    return True

def check_docker():
    """检查Docker环境"""
    print("\n" + "=" * 50)
    print("  Docker环境检查")
    print("=" * 50)
    
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Docker已安装")
            print(f"  版本: {result.stdout.strip()}")
            return True
        else:
            print("\n✗ Docker未安装或未运行")
            return False
    except Exception as e:
        print(f"\n✗ Docker检查失败: {e}")
        return False

def check_buildozer_image():
    """检查Buildozer Docker镜像"""
    print("\n" + "=" * 50)
    print("  Buildozer镜像检查")
    print("=" * 50)
    
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "images"],
            capture_output=True,
            text=True
        )
        
        if "kivy/buildozer" in result.stdout:
            print("\n✓ Buildozer镜像已下载")
            return True
        else:
            print("\n✗ Buildozer镜像未下载")
            print("\n请运行: docker pull kivy/buildozer")
            return False
    except Exception as e:
        print(f"\n✗ Buildozer镜像检查失败: {e}")
        return False

def check_project_files():
    """检查项目文件"""
    print("\n" + "=" * 50)
    print("  项目文件检查")
    print("=" * 50)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = [
        "btc_5min_kivy.py",
        "buildozer.spec",
        "main.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for file in required_files:
        file_path = os.path.join(project_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} 不存在")
            all_exist = False
    
    return all_exist

def print_build_instructions():
    """打印构建说明"""
    print("\n" + "=" * 50)
    print("  构建说明")
    print("=" * 50)
    
    print("\n由于当前环境的Docker命令无法正常工作，")
    print("建议使用以下方法之一来构建APK：")
    
    print("\n方法一：使用GitHub Actions（推荐）")
    print("  1. 将代码推送到GitHub仓库")
    print("  2. 在GitHub上启用Actions")
    print("  3. 手动触发构建或等待自动构建")
    print("  4. 从Actions页面下载生成的APK文件")
    
    print("\n方法二：使用云服务器")
    print("  1. 租用云服务器（阿里云/腾讯云/华为云）")
    print("  2. 安装Docker")
    print("  3. 上传项目文件")
    print("  4. 运行构建命令")
    
    print("\n方法三：使用GitHub Codespaces")
    print("  1. 在GitHub仓库创建Codespace")
    print("  2. 在浏览器中运行构建命令")
    print("  3. 下载生成的APK文件")
    
    print("\n构建命令：")
    print("  docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug")
    
    print("\n构建时间：")
    print("  首次构建：30-60分钟")
    print("  后续构建：10-20分钟")
    
    print("\n构建完成后，APK文件将位于：")
    print("  bin/目录")
    print("  文件名格式：btc5min-1.0-armeabi-v7a-debug.apk")

def main():
    """主函数"""
    # 检查APK文件
    apk_exists = check_apk_files()
    
    if apk_exists:
        print("\n" + "=" * 50)
        print("✓ APK构建成功！")
        print("=" * 50)
        return True
    
    # APK文件不存在，检查构建环境
    print("\nAPK文件尚未构建，检查构建环境...")
    
    docker_ok = check_docker()
    image_ok = check_buildozer_image()
    files_ok = check_project_files()
    
    print("\n" + "=" * 50)
    print("  环境检查总结")
    print("=" * 50)
    print(f"\nDocker环境: {'✓' if docker_ok else '✗'}")
    print(f"Buildozer镜像: {'✓' if image_ok else '✗'}")
    print(f"项目文件: {'✓' if files_ok else '✗'}")
    
    if docker_ok and image_ok and files_ok:
        print("\n✓ 构建环境已就绪")
        print("\n由于当前环境的Docker命令无法正常工作，")
        print("请参考以下说明进行构建：")
    else:
        print("\n✗ 构建环境未就绪")
        print("\n请先解决上述问题，然后尝试构建APK")
    
    print_build_instructions()
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)