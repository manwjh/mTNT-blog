---
layout: post
title: "mTNT OS 入门指南 - 从零开始搭建开发环境"
date: 2025-08-27 10:00:00 +0800
categories: [Guide, Tutorial]
tags: [mTNT, AI, OS, Guide, Setup, Environment, LLM]
author: 深圳王哥
---

# mTNT OS 入门指南 - 从零开始搭建开发环境

**文档创建日期**: 2025-08-27  
**文档版本**: v1.0.0  
**适用对象**: 开发者、技术爱好者

---

## 1. 项目简介

mTNT OS (mini Touch and Talk Operating System) 是一个基于LLM技术的AI操作系统项目，旨在通过自然语言交互和触摸控制来重新定义人机交互体验。

### 1.1 核心特性
- 🤖 **AI驱动**: 基于大语言模型的智能交互
- 🖐️ **触摸控制**: 直观的触摸手势操作
- 🗣️ **语音交互**: 自然语言对话
- 🔒 **隐私保护**: 本地化AI推理
- 🐧 **Linux生态**: 基于Linux内核

### 1.2 技术栈
- **操作系统**: Linux (Ubuntu/CentOS)
- **编程语言**: Python 3.8+
- **AI框架**: 支持多种LLM模型
- **交互技术**: 触摸屏、语音识别
- **部署方式**: 本地化 + 云端混合

---

## 2. 系统要求

### 2.1 硬件要求
- **CPU**: 4核心以上 (推荐8核心)
- **内存**: 8GB+ (推荐16GB)
- **存储**: 20GB+ 可用空间
- **网络**: 稳定的互联网连接

### 2.2 软件要求
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / macOS 10.15+
- **Python**: 3.8+ 版本
- **Git**: 最新版本
- **Docker**: 可选，用于容器化部署

---

## 3. 环境搭建步骤

### 3.1 克隆项目

```bash
# 克隆主项目
git clone https://github.com/manwjh/mTNT-aios.git
cd mTNT-aios

# 克隆博客项目（可选）
git clone https://github.com/manwjh/mTNT-blog.git
cd mTNT-blog
```

### 3.2 创建Python虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3.3 安装依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装开发工具
pip install pytest black flake8 mypy
```

### 3.4 配置环境变量

创建 `.env` 文件：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

配置内容示例：

```env
# 项目配置
PROJECT_NAME=mTNT-OS
DEBUG=True
LOG_LEVEL=INFO

# AI模型配置
LLM_MODEL_PATH=/path/to/your/model
LLM_API_KEY=your_api_key_here

# 数据库配置
DATABASE_URL=sqlite:///mtnt.db

# 网络配置
HOST=0.0.0.0
PORT=8000
```

---

## 4. 首次运行

### 4.1 启动开发服务器

```bash
# 启动主服务
python main.py

# 或者使用开发模式
python -m flask run --debug
```

### 4.2 验证安装

访问以下地址验证服务是否正常：

- **主界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 4.3 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_core.py

# 生成测试覆盖率报告
pytest --cov=mtnt_core
```

---

## 5. 开发工作流

### 5.1 代码规范

项目使用以下工具确保代码质量：

```bash
# 代码格式化
black mtnt_core/

# 代码检查
flake8 mtnt_core/

# 类型检查
mypy mtnt_core/
```

### 5.2 Git工作流

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin feature/new-feature

# 创建Pull Request
# 在GitHub上创建PR
```

### 5.3 调试技巧

```bash
# 启用调试模式
export DEBUG=True

# 查看详细日志
export LOG_LEVEL=DEBUG

# 使用Python调试器
python -m pdb main.py
```

---

## 6. 常见问题解决

### 6.1 依赖安装失败

```bash
# 清理缓存
pip cache purge

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 6.2 权限问题

```bash
# 修复权限
sudo chown -R $USER:$USER /path/to/project

# 或者使用用户安装
pip install --user -r requirements.txt
```

### 6.3 端口占用

```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

---

## 7. 下一步

### 7.1 学习资源
- 📖 [项目文档](https://github.com/manwjh/mTNT-aios/wiki)
- 🎥 [视频教程](https://www.youtube.com/playlist?list=...)
- 💬 [社区讨论](https://github.com/manwjh/mTNT-aios/discussions)

### 7.2 贡献指南
- 🐛 [报告Bug](https://github.com/manwjh/mTNT-aios/issues)
- ✨ [功能建议](https://github.com/manwjh/mTNT-aios/discussions)
- 📝 [文档改进](https://github.com/manwjh/mTNT-aios/wiki)

### 7.3 联系方式
- **GitHub**: [manwjh/mTNT-aios](https://github.com/manwjh/mTNT-aios)
- **Twitter**: [@cpswang](https://x.com/cpswang)
- **Email**: contact@mtnt-os.com

---

## 8. 总结

通过本指南，你已经成功搭建了mTNT OS的开发环境。接下来你可以：

1. **探索代码结构**: 了解项目的整体架构
2. **运行示例**: 尝试运行项目提供的示例
3. **参与开发**: 选择感兴趣的功能进行开发
4. **加入社区**: 与其他开发者交流经验

**记住**: 开发是一个持续学习的过程，遇到问题时不要犹豫，随时在社区中寻求帮助！

---

*本文档会持续更新，请关注项目的最新动态。*

**相关链接**:
- [mTNT OS 项目主页](https://github.com/manwjh/mTNT-aios)
- [开发指南索引](../guides.html)
- [常见问题解答](../issues.html)
