#!/bin/bash

# mTNT Blog 部署脚本
# 用于自动化部署到GitHub Pages

echo "🚀 开始部署 mTNT Blog..."

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 发现未提交的更改，请先提交所有更改"
    git status
    exit 1
fi

# 构建网站
echo "📦 构建网站..."
bundle exec jekyll build

# 检查构建是否成功
if [ $? -ne 0 ]; then
    echo "❌ 构建失败"
    exit 1
fi

echo "✅ 构建成功"

# 添加所有更改
echo "📝 添加更改到git..."
git add .

# 提交更改
echo "💾 提交更改..."
git commit -m "deploy: 自动部署更新 $(date '+%Y-%m-%d %H:%M:%S')"

# 推送到远程仓库
echo "🚀 推送到GitHub..."
git push origin main

echo "✅ 部署完成！"
echo "🌐 网站地址: https://manwjh.github.io/mTNT-blog/"
echo "⏰ 部署时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "📝 注意: GitHub Pages 可能需要几分钟时间来更新网站内容"
