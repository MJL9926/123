#!/bin/bash

# Docker构建脚本 - 用于构建Android APK

set -e

echo "========================================="
echo "  BTC 5分钟预测 - Android APK 构建脚本"
echo "========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker服务是否运行
if ! docker info &> /dev/null; then
    echo "错误: Docker服务未运行"
    echo "请启动Docker服务"
    exit 1
fi

echo "Docker环境检查通过"
echo ""

# 设置项目目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "项目目录: $PROJECT_DIR"
echo ""

# 检查buildozer.spec文件
if [ ! -f "$PROJECT_DIR/buildozer.spec" ]; then
    echo "错误: 未找到buildozer.spec文件"
    echo "请确保在项目根目录下运行此脚本"
    exit 1
fi

echo "找到buildozer.spec配置文件"
echo ""

# 拉取Buildozer Docker镜像
echo "正在拉取Buildozer Docker镜像..."
docker pull kivy/buildozer

if [ $? -ne 0 ]; then
    echo "错误: 拉取Docker镜像失败"
    exit 1
fi

echo "Docker镜像拉取成功"
echo ""

# 清理旧的构建文件
echo "清理旧的构建文件..."
docker run --rm -v "$PROJECT_DIR:/home/user/app" kivy/buildozer buildozer android clean

# 构建APK
echo "========================================="
echo "开始构建Android APK..."
echo "========================================="
echo ""

docker run --rm -v "$PROJECT_DIR:/home/user/app" kivy/buildozer buildozer android debug

if [ $? -ne 0 ]; then
    echo "错误: APK构建失败"
    exit 1
fi

echo ""
echo "========================================="
echo "APK构建成功！"
echo "========================================="
echo ""

# 查找生成的APK文件
APK_FILE=$(find "$PROJECT_DIR/bin" -name "*.apk" -type f | head -n 1)

if [ -n "$APK_FILE" ]; then
    echo "APK文件位置: $APK_FILE"
    echo ""
    echo "您可以将此APK文件传输到Android设备进行安装"
    echo ""
    
    # 显示APK文件信息
    APK_SIZE=$(du -h "$APK_FILE" | cut -f1)
    echo "APK文件大小: $APK_SIZE"
    echo ""
    
    echo "安装方法："
    echo "1. 将APK文件传输到Android设备"
    echo "2. 在Android设备上启用'未知来源'应用安装"
    echo "3. 点击APK文件进行安装"
    echo ""
else
    echo "警告: 未找到APK文件"
    echo "请检查构建日志"
    exit 1
fi

echo "========================================="
echo "构建完成！"
echo "========================================="