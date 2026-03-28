#!/usr/bin/env python3
"""
APK构建脚本
使用Docker和Buildozer构建Android APK
"""

import subprocess
import sys
import os
import time

def run_docker_command(cmd, description=""):
    """运行Docker命令"""
    if description:
        print(f"\n{description}")
        print("=" * 50)
    
    print(f"执行命令: {cmd}")
    print()
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        
        if return_code == 0:
            print(f"\n✓ {description} 完成")
            return True
        else:
            print(f"\n✗ {description} 失败 (返回码: {return_code})")
            return False
            
    except Exception as e:
        print(f"命令执行失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("  BTC 5分钟预测 - Android APK 构建")
    print("=" * 50)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n项目目录: {project_dir}")
    
    # 检查Docker
    print("\n检查Docker环境...")
    if not run_docker_command("docker --version", "检查Docker"):
        print("\n✗ Docker未安装或未运行")
        return False
    
    # 检查Buildozer镜像
    print("\n检查Buildozer镜像...")
    if not run_docker_command("docker images | findstr buildozer", "检查镜像"):
        print("\n✗ Buildozer镜像未下载")
        print("\n正在下载Buildozer镜像...")
        if not run_docker_command("docker pull kivy/buildozer", "下载镜像"):
            return False
    
    # 清理旧构建
    print("\n清理旧构建...")
    run_docker_command(
        f'docker run --rm -v "{project_dir}:/home/user/app" kivy/buildozer buildozer android clean',
        "清理构建"
    )
    
    # 构建APK
    print("\n" + "=" * 50)
    print("开始构建Android APK")
    print("=" * 50)
    print("\n注意: 首次构建需要下载大量依赖，可能需要30-60分钟")
    print("请耐心等待...\n")
    
    start_time = time.time()
    
    # 使用Windows路径格式
    success = run_docker_command(
        f'docker run --rm -v "{project_dir}:/home/user/app" kivy/buildozer buildozer android debug',
        "构建APK"
    )
    
    end_time = time.time()
    build_time = end_time - start_time
    
    print(f"\n构建时间: {build_time/60:.1f} 分钟")
    
    if success:
        # 检查APK文件
        bin_dir = os.path.join(project_dir, "bin")
        if os.path.exists(bin_dir):
            apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
            if apk_files:
                print("\n" + "=" * 50)
                print("✓ APK构建成功！")
                print("=" * 50)
                print(f"\n找到 {len(apk_files)} 个APK文件:")
                for apk in apk_files:
                    apk_path = os.path.join(bin_dir, apk)
                    size = os.path.getsize(apk_path)
                    size_mb = size / (1024 * 1024)
                    print(f"  - {apk} ({size_mb:.1f} MB)")
                
                print("\n安装方法:")
                print("1. 将APK文件传输到Android设备")
                print("2. 在Android设备上启用'未知来源'应用安装")
                print("3. 点击APK文件进行安装")
                return True
        
        print("\n警告: 构建成功但未找到APK文件")
        return False
    else:
        print("\n✗ APK构建失败")
        print("\n可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 增加Docker内存限制")
        print("3. 清理Docker缓存: docker system prune -a")
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