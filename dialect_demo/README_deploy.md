# 🎙️ 方言采集系统 - 宝塔面板部署指南

## 📦 部署包内容

```
dialect_demo_deploy/
├── app.py                      # 主程序
├── database.py                 # 数据库操作
├── models.py                   # 数据模型
├── requirements.txt            # Python 依赖
├── templates/                  # HTML 模板
├── static/                     # 静态文件
└── README_deploy.md           # 本文件
```

---

## 🚀 宝塔面板部署步骤

### 1️⃣ 创建网站

1. 登录宝塔面板
2. 点击"网站" → "添加站点"
3. 填写域名：`dialect.yourdomain.com`（你的二级域名）
4. 数据库：MySQL（或直接用 SQLite）
5. PHP 版本：纯 Python 项目，无需 PHP
6. 点击"提交"

### 2️⃣ 上传代码

1. 进入"文件" → 找到网站根目录（如 `/www/wwwroot/dialect.yourdomain.com`）
2. 上传所有代码文件
3. 解压（如果是 ZIP 包）

### 3️⃣ 安装 Python 环境

1. 在宝塔"软件商店"安装 **Python 项目管理器**
2. 进入"Python 项目管理器"
3. 点击"添加项目"
   - 项目名称：`dialect_demo`
   - 项目路径：`/www/wwwroot/dialect.yourdomain.com`
   - Python 版本：3.8+（推荐 3.9）
   - 启动文件：`app.py`
   - 端口：`5001`（或其他空闲端口）
4. 点击"提交"

### 4️⃣ 安装依赖

在 Python 项目管理器中：
1. 找到刚创建的项目
2. 点击"管理"
3. 进入"依赖管理"
4. 点击"安装依赖"（会自动读取 requirements.txt）

或手动执行：
```bash
cd /www/wwwroot/dialect.yourdomain.com
pip3 install -r requirements.txt
```

### 5️⃣ 启动项目

1. 在 Python 项目管理器中点击"启动"
2. 状态显示"运行中"即成功

### 6️⃣ 配置反向代理

1. 进入"网站" → 找到你的站点
2. 点击"设置" → "反向代理"
3. 添加反向代理：
   - 代理名称：`dialect_proxy`
   - 目标 URL：`http://127.0.0.1:5001`
   - 发送域名：`$host`
4. 点击"提交"

### 7️⃣ 配置 SSL（可选）

1. 进入"网站" → 找到你的站点
2. 点击"设置" → "SSL"
3. 选择"Let's Encrypt"免费证书
4. 申请并启用

---

## 🔧 生产环境配置

### 修改 app.py

将这段代码：
```python
if __name__ == '__main__':
    init_db(app)
    app.run(debug=True, host='0.0.0.0', port=5001)
```

改为：
```python
if __name__ == '__main__':
    init_db(app)
    app.run(debug=False, host='0.0.0.0', port=5001)
```

**⚠️ 重要：生产环境不要开启 debug 模式！**

### 修改数据库路径（可选）

如果需要固定数据库位置，在 `app.py` 中添加：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////www/wwwroot/dialect.yourdomain.com/instance/dialect_demo.db'
```

---

## 🔐 默认账号

**管理员账号：**
- 手机号：`13800000000`
- 密码：`123456`

**⚠️ 首次登录后建议修改密码！**

---

## 📝 常见问题

### Q1: 端口被占用
**解决：** 修改 `app.py` 中的端口号（如 5002、5003）

### Q2: 权限不足
**解决：** 
```bash
chmod -R 755 /www/wwwroot/dialect.yourdomain.com
chown -R www:www /www/wwwroot/dialect.yourdomain.com
```

### Q3: 无法访问
**检查：**
1. 宝塔防火墙是否放行端口
2. 安全组是否开放端口（云服务器）
3. Python 项目是否运行中

### Q4: 数据库初始化失败
**解决：** 
```bash
# 删除数据库文件重新初始化
rm -rf /www/wwwroot/dialect.yourdomain.com/instance/
# 重启 Python 项目
```

---

## 📊 目录权限设置

```bash
# 设置网站目录权限
chmod -R 755 /www/wwwroot/dialect.yourdomain.com

# 设置 uploads 目录可写
chmod -R 777 /www/wwwroot/dialect.yourdomain.com/static/uploads

# 设置 instance 目录可写
chmod -R 777 /www/wwwroot/dialect.yourdomain.com/instance
```

---

## 🔄 日常维护

### 查看日志
```bash
tail -f /www/wwwroot/dialect.yourdomain.com/logs/error.log
```

### 重启服务
在宝塔 Python 项目管理器中点击"重启"

### 备份数据库
```bash
cp /www/wwwroot/dialect.yourdomain.com/instance/dialect_demo.db \
   /www/wwwroot/dialect.yourdomain.com/instance/dialect_demo.db.backup.$(date +%Y%m%d)
```

---

## 📞 部署完成后

1. 访问域名测试：`http://dialect.yourdomain.com`
2. 用管理员账号登录
3. 测试完整流程
4. 如有问题，截图发给我

---

**部署时间：** 预计 10-15 分钟  
**难度：** ⭐⭐（简单）
