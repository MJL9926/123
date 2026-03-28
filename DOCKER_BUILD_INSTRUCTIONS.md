# Docker构建Android APK - 完整指南

## 当前环境状态

由于当前Windows环境的Docker和WSL服务无法正常工作，建议使用以下替代方案进行构建。

## 方案一：使用在线Docker服务（推荐）

### 使用GitHub Codespaces

1. **创建GitHub仓库**
   - 将项目代码推送到GitHub
   - 确保包含所有必要文件

2. **打开Codespaces**
   - 在GitHub仓库页面点击 "Code" 按钮
   - 选择 "Codespaces" 标签
   - 点击 "Create codespace on main"

3. **在Codespaces中构建**
   ```bash
   # 安装Docker（如果未安装）
   sudo apt update
   sudo apt install -y docker.io
   
   # 启动Docker服务
   sudo service docker start
   
   # 拉取Buildozer镜像
   docker pull kivy/buildozer
   
   # 构建APK
   docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug
   ```

4. **下载APK**
   - 构建完成后，APK文件位于 `bin/` 目录
   - 右键点击APK文件，选择 "Download" 下载到本地

## 方案二：使用云服务器构建

### 使用阿里云/腾讯云/华为云服务器

1. **创建云服务器实例**
   - 选择Ubuntu 20.04或更高版本
   - 配置：至少2核4G，建议4核8G
   - 磁盘：至少50GB

2. **连接服务器**
   ```bash
   ssh root@your-server-ip
   ```

3. **安装依赖**
   ```bash
   # 更新系统
   apt update && apt upgrade -y
   
   # 安装必要软件
   apt install -y build-essential git python3 python3-dev \
       openjdk-17-jdk unzip zip libffi-dev libssl-dev docker.io
   
   # 启动Docker
   systemctl start docker
   systemctl enable docker
   ```

4. **上传项目文件**
   ```bash
   # 在本地使用scp上传
   scp -r /path/to/project root@your-server-ip:/root/btc_5min
   ```

5. **构建APK**
   ```bash
   cd /root/btc_5min
   docker pull kivy/buildozer
   docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug
   ```

6. **下载APK**
   ```bash
   # 在服务器上
   scp root@your-server-ip:/root/btc_5min/bin/*.apk ./
   ```

## 方案三：使用本地Linux虚拟机

### 使用VirtualBox + Ubuntu

1. **安装VirtualBox**
   - 下载地址：https://www.virtualbox.org/wiki/Downloads

2. **创建Ubuntu虚拟机**
   - 下载Ubuntu 20.04 ISO
   - 创建虚拟机，分配至少4GB内存和50GB磁盘

3. **在虚拟机中构建**
   ```bash
   # 安装Docker
   sudo apt update
   sudo apt install -y docker.io
   sudo usermod -aG docker $USER
   
   # 重启或重新登录
   newgrp docker
   
   # 共享文件夹设置
   # 在VirtualBox中设置共享文件夹，将项目目录挂载到虚拟机
   
   # 构建APK
   cd /path/to/shared/project
   docker pull kivy/buildozer
   docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug
   ```

## 方案四：使用Docker Desktop（Windows本地）

### 安装和配置

1. **安装Docker Desktop**
   - 下载地址：https://www.docker.com/products/docker-desktop
   - 安装时启用WSL2后端

2. **配置Docker**
   - 打开Docker Desktop设置
   - Resources > WSL Integration：启用Ubuntu
   - 增加内存限制到至少4GB

3. **在WSL中构建**
   ```bash
   # 打开WSL终端
   wsl
   
   # 进入项目目录
   cd /mnt/c/Users/Administrator/Desktop/5分钟/5版本4
   
   # 拉取镜像并构建
   docker pull kivy/buildozer
   docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug
   ```

## 构建配置优化

### 减小APK大小

编辑 `buildozer.spec`：

```ini
# 只构建一个架构
android.arch = armeabi-v7a

# 或
android.arch = arm64-v8a
```

### 加速构建

```ini
# 使用国内镜像（在中国大陆）
# 在Docker运行前设置
export DOCKER_BUILDKIT=1
```

## 常见问题解决

### 1. 构建失败：内存不足

```bash
# 增加swap空间
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 2. 构建失败：网络超时

```bash
# 使用代理
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080

# 或使用国内镜像
docker pull registry.cn-hangzhou.aliyuncs.com/kivy/buildozer
```

### 3. 构建失败：权限问题

```bash
# 修复权限
sudo chown -R $(whoami):$(whoami) .
```

### 4. WSL错误

```bash
# 重启WSL
wsl --shutdown
wsl

# 或重置WSL
wsl --unregister Ubuntu
wsl --install -d Ubuntu
```

## 验证构建

### 检查APK文件

```bash
# 查看APK信息
aapt dump badging your-app.apk

# 检查签名
jarsigner -verify -verbose -certs your-app.apk
```

### 安装测试

```bash
# 使用adb安装
adb install your-app.apk

# 或使用Android Studio的设备管理器
```

## 自动化构建脚本

创建 `build.sh`：

```bash
#!/bin/bash
set -e

echo "开始构建Android APK..."

# 清理旧构建
docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android clean

# 构建APK
docker run --rm -v $(pwd):/home/user/app kivy/buildozer buildozer android debug

# 检查构建结果
if [ -f "bin/*.apk" ]; then
    echo "✓ 构建成功！"
    ls -lh bin/*.apk
else
    echo "✗ 构建失败"
    exit 1
fi
```

## 技术支持

如遇到问题，请提供：
1. 操作系统版本
2. Docker版本
3. 完整的错误日志
4. buildozer.spec配置文件
5. 网络环境（是否在中国大陆）

## 参考资源

- [Buildozer官方文档](https://buildozer.readthedocs.io/)
- [Kivy官方文档](https://kivy.org/doc/stable/)
- [Docker官方文档](https://docs.docker.com/)
- [Python for Android](https://python-for-android.readthedocs.io/)