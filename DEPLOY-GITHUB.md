# 📦 方言语音采集系统 - GitHub 自动部署指南

## 🎯 目标

配置服务器自动从 GitHub 拉取代码，实现自动更新。

---

## 📋 前提条件

- 服务器已安装 Git
- 服务器可以访问 GitHub（`github.com`）

---

## 🔧 部署步骤

### 第 1 步：在服务器上操作

**SSH 登录服务器后执行：**

```bash
# 1. 进入网站根目录（根据实际情况修改路径）
cd /path/to/your/website

# 2. 备份现有代码（重要！）
cp -r . /tmp/website-backup-$(date +%Y%m%d)

# 3. 初始化 Git（如果已有 .git 文件夹，先删除）
rm -rf .git
git init

# 4. 配置远程仓库
git remote add origin https://github.com/yzxr/dialect-recording-system.git

# 5. 拉取最新代码
git fetch origin
git reset --hard origin/main

# 6. 检查文件权限（确保 Web 服务器可读写）
chown -R www:www /path/to/your/website
chmod -R 755 /path/to/your/website
```

---

### 第 2 步：配置自动更新（推荐）

**方案 A：使用 Cron 定时任务（简单）**

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 5 分钟自动拉取更新）
*/5 * * * * cd /path/to/your/website && git fetch origin && git reset --hard origin/main >> /tmp/git-deploy.log 2>&1
```

**方案 B：手动拉取（按需更新）**

每次需要更新时，执行：
```bash
cd /path/to/your/website
git fetch origin
git reset --hard origin/main
```

---

## 🧪 验证部署

1. 访问网站，确认页面正常加载
2. 检查录音上传功能是否正常
3. 查看今日录音列表是否显示

---

## 📝 注意事项

### 1. 配置文件保护

如果服务器上有本地配置文件（如数据库密码），建议：

- 将配置文件添加到 `.gitignore`
- 或者在服务器上手动修改后，执行 `git update-index --assume-unchanged config.php`

### 2. 数据库迁移

如果数据库结构有变更，需要手动执行：

```bash
# 导入数据库结构
mysql -u 用户名 -p 数据库名 < database.sql
```

### 3. 回滚方案

如果更新后出现问题，可以快速回滚：

```bash
# 恢复到上一个版本
git reset --hard HEAD~1

# 或者恢复到指定版本
git reset --hard <commit-hash>
```

---

## 🔐 安全建议

### 使用 SSH 密钥（可选，更安全）

如果不想在 URL 中暴露 Token，可以使用 SSH 密钥：

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "server-deploy"

# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 3. 将公钥添加到 GitHub
# 访问：https://github.com/settings/keys
# 点击 "New SSH key"，粘贴公钥

# 4. 修改远程仓库为 SSH 地址
git remote set-url origin git@github.com:yzxr/dialect-recording-system.git
```

---

## 📞 遇到问题？

### 常见问题排查

**1. Git 命令不存在**
```bash
# 安装 Git
# CentOS/RHEL:
yum install git -y

# Ubuntu/Debian:
apt-get install git -y
```

**2. 无法连接 GitHub**
```bash
# 检查网络
ping github.com

# 检查防火墙
# 确保 443 端口（HTTPS）开放
```

**3. 权限错误**
```bash
# 修复文件权限
chown -R www:www /path/to/your/website
chmod -R 755 /path/to/your/website
```

---

## 🚀 更新流程

**日常更新（AI 修改代码后）：**

1. AI 在本地修改代码
2. AI 推送到 GitHub
3. 服务器自动拉取（Cron）或手动拉取
4. 网站即时更新 ✅

**无需人工登录服务器上传文件！**

---

## 📊 仓库信息

- **GitHub 仓库**: https://github.com/yzxr/dialect-recording-system
- **分支**: `main`
- **最后更新**: 2026-04-06

---

**部署完成后，删除本文件中的敏感信息（如 Token、密码等）**
