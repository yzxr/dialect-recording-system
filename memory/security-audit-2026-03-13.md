# 安全审查报告 - 刚哥的 MacBook Air

**审查时间:** 2026-03-13 09:15 CST  
**审查工具:** OpenClaw healthcheck skill  
**系统:** macOS 14.8.4 (Sonoma)

---

## 🚨 关键发现摘要

| 严重程度 | 问题数量 | 状态 |
|---------|---------|------|
| 🔴 严重 (Critical) | 1 | 需立即处理 |
| 🟡 警告 (Warning) | 5 | 建议处理 |
| 🟢 信息 (Info) | 3 | 可选优化 |

---

## 🔴 严重问题 (Critical)

### 1. DingTalk 插件包含危险代码模式

**问题:** `~/.openclaw/extensions/dingtalk/` 插件中存在环境变量收集 + 网络发送的可疑代码

**详情:**
- 文件: `scripts/dingtalk-stream-monitor.mjs` 第 47 行
- 模式: `[env-harvesting]` - 读取环境变量后发送到外部 API
- 代码读取 `DINGTALK_CLIENT_ID`、`DINGTALK_CLIENT_SECRET` 等敏感环境变量
- 向 `https://api.dingtalk.com` 发送网络请求

**风险:** 可能泄露你的钉钉 API 凭证和其他环境变量

**建议:**
```bash
# 选项 1: 删除插件（如果不需要钉钉集成）
rm -rf ~/.openclaw/extensions/dingtalk

# 选项 2: 审查代码后决定是否信任
code ~/.openclaw/extensions/dingtalk/scripts/dingtalk-stream-monitor.mjs
```

---

## 🟡 警告问题 (Warnings)

### 2. macOS 防火墙已关闭

**状态:** `Firewall is disabled (State = 0)`

**风险:** 所有监听端口都对网络开放，增加被攻击面

**建议:**
```bash
# 开启 macOS 防火墙
/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# 或手动：系统设置 → 网络 → 防火墙 → 开启
```

### 3. FileVault 磁盘加密未启用

**状态:** `fdesetup isactive = false`

**风险:** 如果设备丢失/被盗，数据可能被直接读取

**建议:**
```bash
# 开启 FileVault
sudo fdesetup enable -user $(whoami)
# 或：系统设置 → 隐私与安全性 → FileVault → 开启
```

### 4. OpenClaw plugins.allow 未配置

**状态:** `plugins.allow` 为空，任何发现的插件可能自动加载

**风险:** 未授权的插件可能被加载执行

**建议:** 在 `~/.openclaw/openclaw.json` 中添加：
```json
"plugins": {
  "allow": ["feishu"]  // 只信任明确列出的插件
}
```

### 5. OpenClaw 有可用更新

**当前:** pnpm stable channel  
**可用:** npm 2026.3.11

**建议:**
```bash
openclaw update
```

### 6. Time Machine 备份状态未知

**状态:** 当前无备份运行 (`Running = 0`)

**建议:** 确认 Time Machine 已配置并定期备份

---

## 🟢 信息项 (Info)

### 7. 监听端口检查

**开放的端口:**
| 端口 | 进程 | 风险 |
|-----|------|------|
| 18789 | node (OpenClaw Gateway) | ✅ 仅 localhost |
| 18791 | node (OpenClaw) | ✅ 仅 localhost |
| 18792 | node (OpenClaw) | ✅ 仅 localhost |
| 18800 | Google Chrome (浏览器控制) | ✅ 仅 localhost |
| 10808 | xray (代理) | ⚠️ 需确认用途 |
| 5000/7000 | ControlCenter | 🟡 macOS 系统服务 |
| 53317 | LocalSend | 🟡 文件传输应用 |
| 59146 | rapportd | 🟡 macOS 系统服务 |

**评估:** OpenClaw 相关服务正确绑定到 localhost，未暴露到公网 ✅

### 8. Gateway 状态

- Gateway 正在运行 (PID 762)
- WebSocket: `ws://127.0.0.1:18789`
- 日志：`/Users/gang/.openclaw/logs/gateway.log`

### 9. 网络暴露

- 机器似乎仅在本地网络使用
- 未发现公网 IP 直接暴露
- 无端口转发配置

---

## 📋  remediation 修复计划

### 立即执行 (高优先级)

```bash
# 1. 审查或删除 DingTalk 插件
ls -la ~/.openclaw/extensions/dingtalk/
# 如果不需要：rm -rf ~/.openclaw/extensions/dingtalk

# 2. 开启 macOS 防火墙
/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# 3. 更新 OpenClaw
openclaw update

# 4. 配置 plugins.allow
# 编辑 ~/.openclaw/openclaw.json，添加 plugins.allow 字段
```

### 近期执行 (中优先级)

```bash
# 5. 开启 FileVault
sudo fdesetup enable -user $(whoami)

# 6. 确认 Time Machine 备份配置
tmutil destinationinfo
```

### 可选优化 (低优先级)

- 审查 xray 代理用途（端口 10808）
- 确认 LocalSend 是否需要常驻监听

---

## 🔐 安全最佳实践建议

1. **定期运行安全审计:**
   ```bash
   openclaw security audit --deep
   ```

2. **启用定期自动审计 (可选):**
   ```bash
   openclaw cron add --name "healthcheck:security-audit" \
     --command "openclaw security audit" \
     --schedule "0 9 * * 1"  # 每周一 9:00
   ```

3. **凭证管理:**
   - API Key 已存储在 `~/.openclaw/openclaw.json`
   - 确保文件权限：`chmod 600 ~/.openclaw/openclaw.json`
   - 考虑使用 1Password 等密码管理器

4. **访问控制:**
   - 不要在公共网络运行 OpenClaw Gateway
   - 如需远程访问，使用 Tailscale 等零信任网络

---

## 📊 风险评分

| 类别 | 得分 | 说明 |
|-----|------|------|
| 系统安全 | 6/10 | 防火墙/FileVault 未开启 |
| OpenClaw 配置 | 7/10 | 插件策略需收紧 |
| 数据安全 | 7/10 | 备份状态待确认 |
| **总体** | **6.7/10** | **中等风险，建议修复** |

---

**审查人:** 月仙总监 🦞  
**下次审查建议:** 修复后 1 周复查，之后每月一次
