#!/usr/bin/env python3
"""
Docker构建脚本 - 用于构建Android APK
使用Python调用Docker API进行构建
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description=""):
    """运行命令并显示输出"""
    if description:
        print(f"\n{description}")
        print("=" * 50)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def check_docker():
    """检查Docker是否可用"""
    print("检查Docker环境...")
    
    # 尝试不同的Docker命令
    docker_commands = [
        "docker --version",
        "wsl docker --version",
        "docker.exe --version"
    ]
    
    for cmd in docker_commands:
        if run_command(cmd, f"尝试: {cmd}"):
            print("✓ Docker可用")
            return True
    
    print("✗ Docker不可用")
    return False

def pull_docker_image():
    """拉取Buildozer Docker镜像"""
    print("\n拉取Buildozer Docker镜像...")
    
    cmd = "docker pull kivy/buildozer"
    if run_command(cmd, "拉取镜像"):
        print("✓ 镜像拉取成功")
        return True
    else:
        print("✗ 镜像拉取失败")
        return False

def build_apk():
    """构建APK"""
    print("\n开始构建Android APK...")
    print("=" * 50)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Docker命令
    docker_cmd = f'docker run --rm -v "{project_dir}:/home/user/app" kivy/buildozer buildozer android debug'
    
    print(f"执行命令: {docker_cmd}")
    print("\n注意: 首次构建需要下载大量依赖，可能需要30-60分钟")
    print("请耐心等待...\n")
    
    # 执行构建
    start_time = time.time()
    
    try:
        process = subprocess.Popen(
            docker_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 实时输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        end_time = time.time()
        build_time = end_time - start_time
        
        print(f"\n构建时间: {build_time/60:.1f} 分钟")
        
        if return_code == 0:
            print("✓ APK构建成功")
            return True
        else:
            print(f"✗ APK构建失败 (返回码: {return_code})")
            return False
            
    except Exception as e:
        print(f"构建过程出错: {e}")
        return False

def find_apk():
    """查找生成的APK文件"""
    print("\n查找APK文件...")
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(project_dir, "bin")
    
    if not os.path.exists(bin_dir):
        print("✗ bin目录不存在")
        return None
    
    # 查找APK文件
    apk_files = []
    for file in os.listdir(bin_dir):
        if file.endswith('.apk'):
            apk_files.append(os.path.join(bin_dir, file))
    
    if apk_files:
        print(f"✓ 找到 {len(apk_files)} 个APK文件:")
        for apk in apk_files:
            size = os.path.getsize(apk)
            size_mb = size / (1024 * 1024)
            print(f"  - {os.path.basename(apk)} ({size_mb:.1f} MB)")
        return apk_files
    else:
        print("✗ 未找到APK文件")
        return None

def main():
    """主函数"""
    print("=" * 50)
    print("  BTC 5分钟预测 - Android APK 构建工具")
    print("=" * 50)
    
    # 检查Docker
    if not check_docker():
        print("\n错误: Docker不可用")
        print("\n解决方案:")
        print("1. 安装Docker Desktop: https://www.docker.com/products/docker-desktop")
        print("2. 启动Docker服务")
        print("3. 重新运行此脚本")
        return False
    
    # 拉取镜像
    if not pull_docker_image():
        print("\n错误: 无法拉取Docker镜像")
        print("请检查网络连接和Docker配置")
        return False
    
    # 构建APK
    if not build_apk():
        print("\n错误: APK构建失败")
        print("\n可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 增加Docker内存限制")
        print("3. 清理Docker缓存: docker system prune -a")
        return False
    
    # 查找APK
    apk_files = find_apk()
    
    if apk_files:
        print("\n" + "=" * 50)
        print("✓ 构建完成！")
        print("=" * 50)
        print("\n安装方法:")
        print("1. 将APK文件传输到Android设备")
        print("2. 在Android设备上启用'未知来源'应用安装")
        print("3. 点击APK文件进行安装")
        print("\n注意: 首次安装可能需要允许安装未知来源应用")
        return True
    else:
        print("\n警告: 构建成功但未找到APK文件")
        print("请检查构建日志")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断构建")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        sys.exit(1)