#!/bin/bash
# 方言采集系统 - 打包脚本
# 用于生成部署包

echo "🎙️ 方言采集系统 - 打包部署包..."

# 创建部署目录
DEPLOY_DIR="dialect_demo_deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# 复制核心文件
cp app_production.py $DEPLOY_DIR/app.py
cp database.py $DEPLOY_DIR/
cp models.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp README_deploy.md $DEPLOY_DIR/

# 复制模板目录
cp -r templates $DEPLOY_DIR/

# 创建空的 static 和 logs 目录
mkdir -p $DEPLOY_DIR/static/uploads
mkdir -p $DEPLOY_DIR/logs
mkdir -p $DEPLOY_DIR/instance

# 创建.gitignore
cat > $DEPLOY_DIR/.gitignore << EOF
# 数据库
instance/*.db
instance/*.db-journal

# 日志
logs/*.log

# 上传文件
static/uploads/*
!static/uploads/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/

# 系统文件
.DS_Store
Thumbs.db
EOF

# 创建空的.gitkeep 文件
touch $DEPLOY_DIR/static/uploads/.gitkeep
touch $DEPLOY_DIR/logs/.gitkeep
touch $DEPLOY_DIR/instance/.gitkeep

# 打包
cd $DEPLOY_DIR
zip -r ../dialect_demo_deploy.zip .
cd ..

echo "✅ 打包完成！"
echo "📦 部署包：dialect_demo_deploy.zip"
echo "📁 部署目录：$DEPLOY_DIR/"
echo ""
echo "📤 上传到宝塔面板："
echo "   1. 登录宝塔面板"
echo "   2. 上传 dialect_demo_deploy.zip 到网站根目录"
echo "   3. 解压"
echo "   4. 在 Python 项目管理器中安装依赖并启动"
echo ""
echo "详细说明请查看：README_deploy.md"
