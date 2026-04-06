# 录音收集平台 - 部署说明

## 📁 文件清单

```
luyin-backend/
├── config.php          # 数据库配置
├── database.sql        # 数据库表结构
├── register.php        # 注册 API
├── login.php           # 登录 API
└── index.html          # 前端页面（登录 + 注册）
```

## 🚀 部署步骤

### 1️⃣ 创建数据库

1. 登录宝塔面板 → 数据库
2. 点击"添加数据库"
3. 数据库名：`luyin_db`
4. 用户名：`root`（或新建用户）
5. 密码：（设置密码）
6. 点击"提交"

或者直接导入 `database.sql`：
- 点击数据库右侧"管理"（phpMyAdmin）
- 选择 `luyin_db` 数据库
- 点击"导入"标签
- 上传 `database.sql` 文件
- 执行

### 2️⃣ 修改数据库配置

编辑 `config.php`，修改数据库连接信息：

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'luyin_db');      // 数据库名
define('DB_USER', 'root');          // 数据库用户名
define('DB_PASS', '你的密码');       // 数据库密码
```

### 3️⃣ 上传文件到服务器

1. 登录宝塔面板 → 文件
2. 进入网站目录：`/www/wwwroot/luyin.fzzyd.com/dialect-audio-collector/`
3. 创建 `api` 文件夹
4. 上传文件：
   - `config.php` → `api/`
   - `register.php` → `api/`
   - `login.php` → `api/`
   - `index.html` → `frontend/`（覆盖原文件）

### 4️⃣ 测试

访问：https://luyin.fzzyd.com/dialect-audio-collector/frontend/index.html

- 测试注册功能
- 测试登录功能

## 📋 注册字段

- 姓名（必填）
- 手机号（必填，作为登录账号）
- 公司（必填）
- 工号（必填）
- 邮箱（必填）
- 密码（必填，至少 6 位）

## 🔐 登录方式

- 账号：手机号
- 密码：注册时设置的密码

## ⚠️ 注意事项

1. 确保服务器 PHP 版本 ≥ 7.0
2. 确保 MySQL/MariaDB 已安装
3. 确保 `pdo_mysql` 扩展已启用
4. 如遇跨域问题，检查 `config.php` 中的 CORS 设置

## 📞 需要帮助？

有问题联系技术人员或查看宝塔面板日志。
