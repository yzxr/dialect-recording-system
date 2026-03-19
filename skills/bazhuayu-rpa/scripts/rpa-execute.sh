#!/bin/bash
# 八爪鱼 RPA 任务执行脚本

# 配置变量（从环境变量读取）
API_KEY="${BAZHUAYU_API_KEY:-}"
ACCOUNT_ID="${BAZHUAYU_ACCOUNT_ID:-}"
BASE_URL="https://api.rpa.bazhuayu.com"

# 参数检查
if [ -z "$API_KEY" ] || [ -z "$ACCOUNT_ID" ]; then
    echo "错误：请配置 BAZHUAYU_API_KEY 和 BAZHUAYU_ACCOUNT_ID 环境变量"
    exit 1
fi

if [ -z "$1" ]; then
    echo "用法：$0 <流程 ID 或流程名称>"
    exit 1
fi

FLOW_ID="$1"

# 执行 RPA 流程
echo "正在执行 RPA 流程：$FLOW_ID"

# TODO: 根据八爪鱼官方 API 文档完善以下调用
# 示例 API 调用（需要替换为真实 API）
curl -s -X POST "$BASE_URL/v1/flows/execute" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"accountId\": \"$ACCOUNT_ID\",
    \"flowId\": \"$FLOW_ID\",
    \"async\": true
  }" | jq .

echo ""
echo "任务已提交，请使用 rpa-status.sh 查询执行状态"
