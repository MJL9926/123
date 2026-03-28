@echo off
REM Docker构建脚本 - 用于构建Android APK (Windows版本)

setlocal enabledelayedexpansion

echo =========================================
echo   BTC 5分钟预测 - Android APK 构建脚本
echo =========================================
echo.

REM 检查Docker是否安装
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker未安装
    echo 请先安装Docker: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM 检查Docker服务是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker服务未运行
    echo 请启动Docker Desktop
    pause
    exit /b 1
)

echo Docker环境检查通过
echo.

REM 设置项目目录
set "PROJECT_DIR=%~dp0"
echo 项目目录: %PROJECT_DIR%
echo.

REM 检查buildozer.spec文件
if not exist "%PROJECT_DIR%buildozer.spec" (
    echo 错误: 未找到buildozer.spec文件
    echo 请确保在项目根目录下运行此脚本
    pause
    exit /b 1
)

echo 找到buildozer.spec配置文件
echo.

REM 拉取Buildozer Docker镜像
echo 正在拉取Buildozer Docker镜像...
docker pull kivy/buildozer

if %errorlevel% neq 0 (
    echo 错误: 拉取Docker镜像失败
    pause
    exit /b 1
)

echo Docker镜像拉取成功
echo.

REM 清理旧的构建文件
echo 清理旧的构建文件...
docker run --rm -v "%PROJECT_DIR%:/home/user/app" kivy/buildozer buildozer android clean

REM 构建APK
echo =========================================
echo 开始构建Android APK...
echo =========================================
echo.

docker run --rm -v "%PROJECT_DIR%:/home/user/app" kivy/buildozer buildozer android debug

if %errorlevel% neq 0 (
    echo 错误: APK构建失败
    pause
    exit /b 1
)

echo.
echo =========================================
echo APK构建成功！
echo =========================================
echo.

REM 查找生成的APK文件
set "APK_FILE="
for /f "delims=" %%i in ('dir /s /b "%PROJECT_DIR%bin\*.apk" 2^>nul') do (
    set "APK_FILE=%%i"
    goto :found_apk
)

:found_apk
if defined APK_FILE (
    echo APK文件位置: %APK_FILE%
    echo.
    echo 您可以将此APK文件传输到Android设备进行安装
    echo.
    
    REM 显示APK文件信息
    for %%A in ("%APK_FILE%") do (
        echo APK文件大小: %%~zA 字节
    )
    echo.
    
    echo 安装方法：
    echo 1. 将APK文件传输到Android设备
    echo 2. 在Android设备上启用"未知来源"应用安装
    echo 3. 点击APK文件进行安装
    echo.
) else (
    echo 警告: 未找到APK文件
    echo 请检查构建日志
    pause
    exit /b 1
)

echo =========================================
echo 构建完成！
echo =========================================

pause