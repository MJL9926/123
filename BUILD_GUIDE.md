# Android APK 构建指南

## 方法一：使用GitHub Actions自动构建（推荐）

### 步骤：
1. 将代码推送到GitHub仓库
2. 在GitHub上启用Actions
3. 手动触发构建或等待自动构建
4. 从Actions页面下载生成的APK文件

### 优点：
- 无需本地配置复杂的环境
- 自动化构建流程
- 可重复构建
- 免费使用

## 方法二：使用Linux环境构建

### 系统要求：
- Ubuntu 20.04或更高版本
- 至少8GB RAM
- 至少20GB可用磁盘空间

### 安装步骤：

```bash
# 1. 更新系统
sudo apt update
sudo apt upgrade -y

# 2. 安装系统依赖
sudo apt install -y build-essential git python3 python3-dev openjdk-17-jdk unzip zip libffi-dev libssl-dev

# 3. 安装Python依赖
pip3 install --upgrade pip setuptools wheel
pip3 install buildozer

# 4. 克隆或复制项目文件
cd ~
mkdir btc_5min
cd btc_5min
# 复制项目文件到此目录

# 5. 构建APK
buildozer android debug
```

### 构建时间：
- 首次构建：30-60分钟
- 后续构建：10-20分钟

### 输出位置：
APK文件位于：`bin/` 目录

## 方法三：使用Docker容器构建

### 前提条件：
- 已安装Docker
- Docker服务正在运行

### 使用预配置的Buildozer Docker镜像：

```bash
# 1. 拉取Buildozer Docker镜像
docker pull kivy/buildozer

# 2. 运行容器并构建
docker run --rm -v $(pwd):/home/user/app kivy/buildozer android debug

# 3. 或者在容器中交互式构建
docker run -it -v $(pwd):/home/user/app kivy/buildozer bash
cd /home/user/app
buildozer android debug
```

### 注意事项：
- 确保项目文件在当前目录
- 构建完成后APK文件会在`bin/`目录中
- 首次构建会下载大量依赖，需要较长时间

## 方法四：使用云构建服务

### CircleCI

创建`.circleci/config.yml`文件：

```yaml
version: 2.1
jobs:
  build:
    docker:
      - image: cimg/python:3.10
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: |
            sudo apt-get update
            sudo apt-get install -y build-essential openjdk-17-jdk unzip zip libffi-dev libssl-dev
            pip install buildozer
      - run:
          name: Build APK
          command: buildozer android debug
      - store_artifacts:
          path: bin
```

## 构建配置说明

### buildozer.spec配置文件

主要配置项：

```ini
[app]
title = BTC 5分钟预测
package.name = btc5min
package.domain = org.btc
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,requests,pandas,numpy,scikit-learn

# 权限配置
android.permissions = INTERNET

# 屏幕方向
android.orientation = portrait

# 构建配置
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.arch = armeabi-v7a,arm64-v8a

fullscreen = 0
```

## 功能验证

### 构建完成后，验证以下功能：

1. **核心预测功能**
   - 应用启动正常
   - 价格数据获取正常
   - 预测功能正常

2. **数据处理功能**
   - K线图显示正常
   - 胜率统计正常
   - 模型训练正常

3. **平台特定功能**
   - 自动交易功能（交易提示模式）
   - 语音播报功能（Android内置语音）

4. **文件操作**
   - 模型文件读写正常
   - 统计数据保存正常

## 常见问题解决

### 1. 构建失败：依赖安装错误

```bash
# 清理缓存重新构建
buildozer android clean
buildozer android debug
```

### 2. 构建失败：内存不足

```bash
# 增加swap空间
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 3. 构建失败：网络问题

```bash
# 使用代理
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
buildozer android debug
```

### 4. APK安装失败

```bash
# 确保APK签名正确
buildozer android release
```

## 性能优化

### 减小APK大小：

```ini
# 在buildozer.spec中添加
android.minapi = 21
android.arch = armeabi-v7a  # 只构建一个架构
```

### 加速构建：

```bash
# 使用缓存
buildozer android debug --use-cache
```

## 安全建议

1. **发布版本**：使用`buildozer android release`构建发布版本
2. **代码混淆**：考虑使用ProGuard或R8进行代码混淆
3. **权限最小化**：只添加必要的权限
4. **网络安全**：使用HTTPS进行网络通信

## 持续集成

### 自动化测试

在构建前运行测试：

```bash
# 在构建前运行测试
python -m pytest tests/
buildozer android debug
```

### 版本管理

使用语义化版本号：

```ini
version = 1.0.0
```

每次发布时更新版本号。

## 支持与反馈

如遇到问题，请提供以下信息：
- 操作系统版本
- Python版本
- Buildozer版本
- 完整的错误日志
- buildozer.spec配置文件

## 许可证

请确保您的应用符合所有适用的许可证要求。