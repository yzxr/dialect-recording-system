# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---
## 心跳保活配置

# 每 2 小时自动心跳（cron 任务），保持会话活跃
# 确保 12 小时内不会进入睡眠状态
- [x] 心跳任务已配置：`0 */2 * * *`（每 2 小时）
- [x] 状态：正常运行中（上次执行 28 分钟前，状态 ok）

---
## Pending Tasks

- [x] 安装 `proactive-agent-lite` skill（已完成）

---
## 技能批量安装任务（⚠️ ClawHub 限流中）

**执行策略：** 每 2-3 小时安装 1 个技能，避免 ClawHub API 限流

**已完成：**
- [x] `skill-guard` - 安装成功
- [x] `self-improving-agent` - 已存在

**待安装（15+ 个）：**
1. [ ] `openclaw-shield` - 主机安全盾牌 ⏳ 限流中
2. [ ] `openclaw-ops-guardrails` - 运维护栏
3. [ ] `openclaw-cli` - OpenClaw CLI 精通
4. [ ] `self-evolving-skill` - 技能自动升级
5. [ ] `skill-scanner` - 环境巡检推荐
6. [ ] `auto-monitor` - 系统健康监控
7. [ ] `auto-workflow` - 工作流自动化
8. [ ] `agent-browser` - 浏览器控制
9. [ ] `lu-auto-deploy` - 自动部署
10. [ ] `ai-web-automation` - 复杂网页自动化
11. [ ] `multi-search-engine-2-0-1` - 17 引擎聚合搜索 ⚠️ VirusTotal  flagged
12. [ ] `file-summary` - 文件摘要分析
13. [ ] `file-organizer-zh` - 文件自动整理
14. [ ] `afrexai-productivity-system` - 个人生产力 OS
15. [ ] `visual-file-sorter` - 视觉文件分类

**新增需求（公众号自动化产线）：**
- [ ] `humanizer` - AI 文本润色
- [ ] `article-illustrator` - 文章配图
- [ ] `capability-evolver` - 能力进化
- [ ] `snews-aggregator-skill` - 全球日报聚合
- [ ] 等...

**限流记录：**
- 09:00-21:40 期间尝试多次 → 全部限流
- 累计等待超过 12 小时，限流仍未解除

**状态：** ⚠️ ClawHub API 限流异常严格，建议手动安装或联系官方
