#!/bin/bash
# 八爪鱼 RPA 流程列表查询脚本

API_KEY="${BAZHUAYU_API_KEY:-}"
ACCOUNT_ID="${BAZHUAYU_ACCOUNT_ID:-}"
BASE_URL="https://api.rpa.bazhuayu.com"

if [ -z "$API_KEY" ] || [ -z "$ACCOUNT_ID" ]; then
    echo "错误：请配置 BAZHUAYU_API_KEY 和 BAZHUAYU_ACCOUNT_ID 环境变量"
    exit 1
fi

echo "获取可用 RPA 流程列表..."

# TODO: 根据八爪鱼官方 API 文档完善以下调用
curl -s -X GET "$BASE_URL/v1/flows?accountId=$ACCOUNT_ID" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" | jq '.data[] | {id: .id, name: .name, status: .status}'
