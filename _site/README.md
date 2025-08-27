# mTNT Blog

基于 mTNT 的技术分享、开发指南和项目记录

## 🌐 在线访问

- **博客地址**: [https://manwjh.github.io/mTNT-blog/](https://manwjh.github.io/mTNT-blog/)
- **GitHub仓库**: [https://github.com/manwjh/mTNT-blog](https://github.com/manwjh/mTNT-blog)

## 📝 项目简介

mTNT Blog 是一个基于 Jekyll 构建的技术博客，主要记录 mTNT OS 项目的开发日志、设计思路和实践经验。

### 项目特色

- 🤖 **AI驱动**: 基于LLM技术的智能操作系统
- 🖐️ **触摸交互**: 自然语言+触摸控制
- 🔒 **隐私保护**: 本地化实现，保护个人隐私
- 🐧 **Linux生态**: 充分发挥Linux软件生态优势
- ☁️ **混合架构**: 支持云端与本地混合部署

## 🚀 本地开发

### 环境要求

- Ruby 2.6+
- Bundler
- Jekyll 3.9+

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/manwjh/mTNT-blog.git
   cd mTNT-blog
   ```

2. **安装依赖**
   ```bash
   bundle install
   ```

3. **启动本地服务器**
   ```bash
   bundle exec jekyll serve --host 127.0.0.1 --port 4000
   ```

4. **访问本地博客**
   打开浏览器访问: http://127.0.0.1:4000/mTNT-blog/

## 📝 添加新文章

### 创建文章

在 `_posts/` 目录下创建新的 Markdown 文件，文件名格式为：`YYYY-MM-DD-title.md`

### 文章模板

```markdown
---
layout: post
title: "文章标题"
date: 2025-08-26 10:00:00 +0800
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
author: 作者名
---

# 文章内容

这里是文章的具体内容...
```

### 文章分类

- **AIOS**: AI操作系统相关
- **Architecture**: 架构设计
- **Technical**: 技术分享
- **Analysis**: 系统分析
- **Project**: 项目介绍

## 🚀 部署

### 自动部署

使用提供的部署脚本：

```bash
./scripts/deploy.sh
```

### 手动部署

1. **构建网站**
   ```bash
   bundle exec jekyll build
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 更新内容"
   git push origin main
   ```

3. **等待GitHub Pages自动构建**
   GitHub Pages 会在推送后自动构建和部署网站

## 📁 项目结构

```
mTNT-blog/
├── _posts/           # 博客文章
├── _pages/           # 静态页面
├── _layouts/         # 布局模板
├── _includes/        # 包含文件
├── assets/           # 静态资源
│   ├── css/         # 样式文件
│   ├── js/          # JavaScript文件
│   └── images/      # 图片资源
├── scripts/          # 脚本文件
├── _site/           # 构建输出目录
├── _config.yml      # Jekyll配置文件
├── Gemfile          # Ruby依赖文件
└── README.md        # 项目说明
```

## 🔧 配置说明

### 主要配置项

- **baseurl**: `/mTNT-blog` - GitHub Pages路径
- **permalink**: `/:year/:month/:day/:title/` - 文章URL格式
- **pagination**: 启用分页功能
- **plugins**: 使用的Jekyll插件

### 自定义配置

可以在 `_config.yml` 中修改以下配置：

- 网站标题和描述
- 作者信息
- 社交媒体链接
- 分页设置
- 主题配置

## 📊 访问统计

博客集成了不蒜子访问统计，可以查看：

- 总访问量
- 访客数
- 页面访问统计

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个博客！

### 贡献方式

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- **GitHub**: [@manwjh](https://github.com/manwjh)
- **Twitter**: [@cpswang](https://x.com/cpswang)
- **项目地址**: [https://github.com/manwjh/mTNT-blog](https://github.com/manwjh/mTNT-blog)

---

**感谢访问 mTNT Blog！** 🚀
