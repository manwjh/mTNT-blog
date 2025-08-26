<<<<<<< HEAD
# mTNT Blog

基于Jekyll构建的mTNT技术博客，记录AI操作系统开发日志、设计思路和实践经验。

## 🚀 项目特色

- 🤖 **AI驱动**: 基于LLM技术的智能操作系统
- 🖐️ **触摸交互**: 自然语言+触摸控制
- 🔒 **隐私保护**: 本地化实现，保护个人隐私
- 🐧 **Linux生态**: 充分发挥Linux软件生态优势
- ☁️ **混合架构**: 支持云端与本地混合部署

## 📖 内容概览

- **技术文章**: mTNT OS架构设计、开发指南
- **开发日志**: 项目进展、技术探索
- **最佳实践**: 开发经验和技巧分享
- **双语支持**: 中英文内容，国际化友好

## 🛠️ 本地开发

### 环境要求

- Ruby 2.7+
- Jekyll 4.0+
- Git

### 安装步骤

1. **克隆项目**
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
bundle exec jekyll serve
```

4. **访问网站**
打开浏览器访问: http://localhost:4000

## 📝 添加新文章

### 文章格式

在`_posts`目录下创建markdown文件，命名格式：`YYYY-MM-DD-title.md`

### Front Matter示例

```yaml
---
layout: post
title: "文章标题"
date: 2024-08-26 10:00:00 +0800
categories: [Technical, AI]
tags: [mTNT, AI, OS, LLM]
author: 深圳王哥
---

# 文章内容

这里是文章内容...
```

### 双语内容

建议每篇文章都包含中英文内容：

```markdown
# 中文标题

中文内容...

---

# English Title

English content...
```

## 🔧 自动化工具

项目包含自动化检查和部署脚本：

```bash
# 检查规范
python3 scripts/check_and_deploy.py -c

# 完整检查和部署
python3 scripts/check_and_deploy.py

# 仅部署
python3 scripts/check_and_deploy.py -d
```

## 📁 项目结构

```
mTNT-blog/
├── _config.yml          # Jekyll配置文件
├── _layouts/            # 布局模板
├── _includes/           # 包含文件
├── _posts/              # 博客文章
├── _guides/             # 开发指南
├── _issues/             # 常见问题
├── _data/               # 数据文件
├── assets/              # 静态资源
│   ├── css/             # 样式文件
│   ├── js/              # JavaScript文件
│   └── images/          # 图片资源
├── scripts/             # 自动化脚本
├── index.md             # 首页
├── about.md             # 关于页面
├── Gemfile              # Ruby依赖
└── README.md            # 项目说明
```

## 🎨 自定义主题

项目使用自定义主题，主要特点：

- 现代化设计风格
- 响应式布局
- 双语内容支持
- SEO优化
- 快速加载

## 🌐 部署

### GitHub Pages

1. 推送代码到GitHub
2. 在仓库设置中启用GitHub Pages
3. 选择部署分支（通常是main或gh-pages）

### 其他平台

支持部署到任何静态网站托管平台：
- Netlify
- Vercel
- GitLab Pages
- 阿里云OSS
- 腾讯云COS

## 🤝 贡献指南

欢迎提交Issue和Pull Request：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 贡献类型

- 🐛 Bug修复
- ✨ 新功能
- 📝 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化

## 📞 联系方式

- **GitHub**: [manwjh/mTNT-blog](https://github.com/manwjh/mTNT-blog)
- **Twitter**: [@cpswang](https://x.com/cpswang)
- **Email**: 通过GitHub Issues联系

## 📄 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

## 🙏 致谢

感谢所有为mTNT项目做出贡献的开发者！

---

**mTNT Blog** - 记录AI操作系统的探索之旅 🚀
=======
# mTNT-blog
>>>>>>> 7d3c7d51856d924eaf6f39191f6e0dd9b4f2610d
