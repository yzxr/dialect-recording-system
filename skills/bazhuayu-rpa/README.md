# 八爪鱼 RPA 技能配置指南

## 第一步：注册八爪鱼账号

1. 访问注册链接：https://partner.rpa.bazhuayu.com/Kdd4Ur
2. 填写企业信息（建议企业身份，审核更快）

## 第二步：申请试用

- 试用申请表单：https://skieer.feishu.cn/share/base/form/shrcnA9np7ot3bE2HYI4ZQggHdg
- 试用期：3 个月

## 第三步：获取 API 密钥

1. 登录八爪鱼 RPA 控制台
2. 进入「设置」→「API 管理」
3. 创建 API Key，记录以下信息：
   - `API_KEY`
   - `ACCOUNT_ID`

## 第四步：配置环境变量

编辑 `~/.zshrc` 或 `~/.bashrc`，添加：

```bash
export BAZHUAYU_API_KEY="你的 API 密钥"
export BAZHUAYU_ACCOUNT_ID="你的账户 ID"
```

然后执行：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

## 第五步：测试技能

```bash
# 列出可用流程
~/.openclaw/workspace/skills/bazhuayu-rpa/scripts/rpa-list.sh

# 执行流程（替换 <流程 ID>）
~/.openclaw/workspace/skills/bazhuayu-rpa/scripts/rpa-execute.sh <流程 ID>

# 查询任务状态
~/.openclaw/workspace/skills/bazhuayu-rpa/scripts/rpa-status.sh <任务 ID>
```

## 常见问题

### Q: 脚本返回空结果？
A: 检查 API 密钥是否正确，网络连接是否正常。

### Q: 权限错误？
A: 确认脚本有执行权限：`chmod +x scripts/*.sh`

### Q: 找不到流程？
A: 确认账户下已创建或订阅了 RPA 流程，可访问应用市场：https://rpa.bazhuayu.com/appstore

## 官方文档

- 官网教程：https://mp.weixin.qq.com/s/fI1xDgPzFQBJs1H9OnuEcA
- 应用市场：https://rpa.bazhuayu.com/appstore
