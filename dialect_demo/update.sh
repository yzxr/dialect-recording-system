#!/bin/bash
# 方言采集系统 - 一键更新脚本
# 使用方法：在宝塔终端中执行 bash update.sh

echo "🎙️ 方言采集系统 - 开始更新..."

# 进入项目目录
cd /www/wwwroot/fy.fzzyd.com

# 备份当前版本
echo "📦 备份当前版本..."
cp database.py database.py.bak
cp app.py app.py.bak
cp models.py models.py.bak
cp -r templates templates.bak

# 下载更新包（从本地上传的/tmp 目录）
if [ -f /tmp/方言采集系统_完整功能更新.zip ]; then
    echo "📥 解压更新包..."
    unzip -o /tmp/方言采集系统_完整功能更新.zip -d /tmp/update_temp/
    
    # 复制更新文件
    cp /tmp/update_temp/database.py .
    cp /tmp/update_temp/app.py .
    cp /tmp/update_temp/models.py .
    cp -r /tmp/update_temp/templates/* templates/
    
    # 清理临时文件
    rm -rf /tmp/update_temp/
    
    echo "✅ 文件更新完成！"
else
    echo "❌ 更新包未找到，请先上传到 /tmp/ 目录"
    exit 1
fi

# 重启 Python 项目
echo "🔄 重启 Python 项目..."
# 在宝塔中手动重启，或执行：
# pm2 restart fangyan (如果使用 PM2)

echo ""
echo "✅ 更新完成！请在宝塔面板中重启 Python 项目"
echo ""
echo "📋 更新内容："
echo "  - 三角色权限系统（系统管理员/团队主管/标注员）"
echo "  - 话术导入去重功能"
echo "  - 话术自动删除（3 天）"
echo "  - 录音文件下载后自动删除"
echo ""
