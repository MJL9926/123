# 使用GitHub Actions构建Android APK - 详细指南

## 为什么使用GitHub Actions？

由于当前Windows环境的Docker命令无法正常工作，使用GitHub Actions是构建Android APK的最佳选择，原因如下：

✅ **无需本地配置** - 不需要在本地安装复杂的构建环境
✅ **自动化构建** - 推送代码后自动触发构建
✅ **免费使用** - GitHub Actions对公开仓库免费
✅ **可靠稳定** - 云端环境稳定，不受本地环境影响
✅ **可重复构建** - 每次推送代码都可以重新构建

## 详细步骤

### 第一步：创建GitHub账号（如果没有）

1. 访问 https://github.com
2. 点击"Sign up"注册账号
3. 完成邮箱验证

### 第二步：创建GitHub仓库

1. 登录GitHub后，点击右上角的"+"号
2. 选择"New repository"
3. 填写仓库信息：
   - Repository name: `btc-5min-prediction`（或您喜欢的名称）
   - Description: `BTC 5分钟预测系统 - Android应用`
   - 选择"Public"（公开）或"Private"（私有）
   - 不要勾选"Initialize this repository with a README"
4. 点击"Create repository"

### 第三步：安装Git工具（如果未安装）

#### Windows用户：

1. 下载Git for Windows: https://git-scm.com/download/win
2. 运行安装程序，使用默认设置
3. 安装完成后，打开Git Bash或命令提示符

#### 验证Git安装：

```bash
git --version
```

### 第四步：配置Git（首次使用）

```bash
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱"
```

### 第五步：初始化本地Git仓库

打开命令提示符或PowerShell，进入项目目录：

```bash
cd C:\Users\Administrator\Desktop\5分钟\5版本4
```

初始化Git仓库：

```bash
git init
```

### 第六步：添加所有文件到Git

```bash
git add .
```

### 第七步：创建首次提交

```bash
git commit -m "初始提交：BTC 5分钟预测系统"
```

### 第八步：关联远程仓库

在GitHub仓库页面，复制仓库的URL（格式：`https://github.com/用户名/仓库名.git`）

```bash
git remote add origin https://github.com/您的用户名/btc-5min-prediction.git
```

### 第九步：推送代码到GitHub

```bash
git branch -M main
git push -u origin main
```

如果提示输入用户名和密码：
- 用户名：输入GitHub用户名
- 密码：输入Personal Access Token（不是GitHub密码）

#### 创建Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 点击"Generate new token" -> "Generate new token (classic)"
3. 勾选权限：
   - `repo`（完整仓库访问权限）
   - `workflow`（工作流权限）
4. 点击"Generate token"
5. 复制生成的token（只显示一次，请妥善保存）

### 第十步：启用GitHub Actions

1. 访问您的GitHub仓库页面
2. 点击"Actions"标签
3. 如果提示启用Actions，点击"I understand my workflows, go ahead and enable them"
4. 点击"New workflow"或查看现有的工作流

### 第十一步：手动触发构建

1. 在仓库页面点击"Actions"标签
2. 在左侧选择"Build Android APK"工作流
3. 点击"Run workflow"
4. 选择分支（main）
5. 点击绿色的"Run workflow"按钮

### 第十二步：查看构建进度

1. 在"Actions"页面，您会看到正在运行的工作流
2. 点击工作流可以查看详细日志
3. 构建时间：首次构建约30-60分钟，后续构建约10-20分钟

### 第十三步：下载APK文件

1. 等待工作流完成（显示绿色✓）
2. 在工作流页面底部找到"Artifacts"部分
3. 点击"android-apk"下载
4. 解压下载的ZIP文件
5. 找到APK文件（位于bin目录）

## APK文件信息

构建成功后，您将获得以下APK文件：

- `btc5min-1.0-armeabi-v7a-debug.apk`（32位ARM设备）
- `btc5min-1.0-arm64-v8a-debug.apk`（64位ARM设备）

根据您的Android设备架构选择相应的APK文件。

## 安装APK到Android设备

### 方法一：通过USB传输

1. 使用USB数据线连接Android设备到电脑
2. 在Android设备上启用"文件传输"模式
3. 将APK文件复制到设备存储
4. 在设备上找到APK文件并点击安装

### 方法二：通过云存储

1. 将APK文件上传到云存储（如Google Drive、百度网盘等）
2. 在Android设备上下载APK文件
3. 点击安装

### 方法三：通过电子邮件

1. 将APK文件作为附件发送到自己的邮箱
2. 在Android设备上打开邮件
3. 下载附件并安装

## 启用"未知来源"应用安装

在Android设备上：

1. 打开"设置"
2. 进入"安全"或"隐私"
3. 找到"允许安装未知来源应用"
4. 启用此选项（可能需要选择允许的应用）

## 常见问题解决

### 问题1：推送代码时认证失败

**解决方案：**
- 确保使用Personal Access Token而不是GitHub密码
- 检查token是否具有`repo`和`workflow`权限

### 问题2：Actions构建失败

**解决方案：**
- 检查Actions日志中的错误信息
- 确保buildozer.spec配置正确
- 检查网络连接

### 问题3：APK安装失败

**解决方案：**
- 确保已启用"未知来源"应用安装
- 检查Android版本是否满足最低要求（API 21+）
- 尝试卸载旧版本后重新安装

### 问题4：应用闪退或功能异常

**解决方案：**
- 检查Android设备日志
- 确保网络连接正常
- 检查应用权限（需要INTERNET权限）

## 更新应用

当您修改代码后：

1. 在本地提交更改：
   ```bash
   git add .
   git commit -m "更新说明"
   git push
   ```

2. GitHub Actions会自动触发构建

3. 下载新的APK文件

4. 在Android设备上安装更新（会覆盖旧版本）

## 工作流配置说明

GitHub Actions工作流文件位于：`.github/workflows/build-android.yml`

主要配置：
- 触发条件：推送到main/master分支或手动触发
- 构建环境：Ubuntu最新版本
- 构建工具：Buildozer
- 输出：bin目录下的APK文件

## 性能优化

### 减小APK大小

编辑`buildozer.spec`：

```ini
# 只构建一个架构
android.arch = armeabi-v7a
```

### 加速构建

使用缓存功能（已在工作流中配置）

## 技术支持

如遇到问题，请提供：
1. GitHub仓库链接
2. Actions工作流链接
3. 错误日志
4. buildozer.spec配置

## 总结

使用GitHub Actions构建Android APK是最简单、最可靠的方法。整个过程包括：

1. 创建GitHub仓库（5分钟）
2. 推送代码（10分钟）
3. 触发构建（1分钟）
4. 等待构建完成（30-60分钟）
5. 下载APK（1分钟）

总计：约1-2小时（首次），后续更新只需10-20分钟构建时间。

祝您构建成功！