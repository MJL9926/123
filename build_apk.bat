@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==================================================
echo   BTC 5分钟预测 - Android APK 构建
echo ==================================================
echo.

echo 项目目录: %CD%
echo.

echo 检查Docker环境...
docker --version
if %errorlevel% neq 0 (
    echo 错误: Docker未安装或未运行
    pause
    exit /b 1
)

echo.
echo 检查Buildozer镜像...
docker images | findstr buildozer
if %errorlevel% neq 0 (
    echo 错误: Buildozer镜像未下载
    echo 正在下载Buildozer镜像...
    docker pull kivy/buildozer
    if %errorlevel% neq 0 (
        echo 错误: 镜像下载失败
        pause
        exit /b 1
    )
)

echo.
echo ==================================================
echo 开始构建Android APK
echo ==================================================
echo.
echo 注意: 首次构建需要下载大量依赖，可能需要30-60分钟
echo 请耐心等待...
echo.

set PROJECT_DIR=%CD%
set DOCKER_CMD=docker run --rm -v "%PROJECT_DIR%:/home/user/app" kivy/buildozer buildozer android debug

echo 执行命令: %DOCKER_CMD%
echo.

%DOCKER_CMD%

if %errorlevel% equ 0 (
    echo.
    echo ==================================================
    echo ✓ APK构建成功！
    echo ==================================================
    echo.
    echo 检查APK文件...
    if exist "bin\*.apk" (
        echo 找到APK文件:
        dir /b bin\*.apk
        echo.
        echo 安装方法:
        echo 1. 将APK文件传输到Android设备
        echo 2. 在Android设备上启用'未知来源'应用安装
        echo 3. 点击APK文件进行安装
    ) else (
        echo 警告: 构建成功但未找到APK文件
        echo 请检查构建日志
    )
) else (
    echo.
    echo ==================================================
    echo ✗ APK构建失败
    echo ==================================================
    echo.
    echo 可能的解决方案:
    echo 1. 检查网络连接
    echo 2. 增加Docker内存限制
    echo 3. 清理Docker缓存: docker system prune -a
)

echo.
pause