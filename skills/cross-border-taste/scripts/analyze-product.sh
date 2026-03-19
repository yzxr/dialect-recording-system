#!/bin/bash
# 跨境选品 Taste 分析快速启动脚本
# 使用方法：./analyze-product.sh [产品链接/关键词]

echo "🔍 跨境选品 Taste 分析"
echo "======================"
echo ""

if [ -z "$1" ]; then
    echo "用法：./analyze-product.sh [产品链接/关键词]"
    echo ""
    echo "示例:"
    echo "  ./analyze-product.sh 'https://amazon.com/dp/xxx'"
    echo "  ./analyze-product.sh 'Japandi style table lamp'"
    exit 1
fi

PRODUCT="$1"

echo "📦 分析对象：$PRODUCT"
echo ""
echo "🧭 三问法分析框架"
echo "----------------"
echo ""
echo "Q1: 这个产品哪里对？"
echo "    → 设计、材质感、主图风格、定价锚点"
echo ""
echo "Q2: 这个产品哪里还差口气？"
echo "    → 站在买家视角，找出犹豫点"
echo ""
echo "Q3: 如果让你改一个地方，改哪里？"
echo "    → 从观察者变成判断者"
echo ""
echo "======================"
echo "💡 提示：将以上问题发给 AI 助手，开始深度分析"
