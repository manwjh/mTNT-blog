# 脚本使用示例

## 快速开始

### 1. 检查当前blog状态

```bash
# 使用Python脚本（推荐）
python3 scripts/check_and_deploy.py -c

# 或使用Bash脚本
./scripts/check_and_deploy.sh -c
```

### 2. 完整检查和部署

```bash
# 使用Python脚本（推荐）
python3 scripts/check_and_deploy.py

# 脚本会询问是否部署，输入 y 确认
```

### 3. 仅部署（跳过检查）

```bash
# 使用Python脚本
python3 scripts/check_and_deploy.py -d
```

## 实际使用场景

### 场景1: 写完新文章后检查

```bash
# 1. 创建新文章
echo "---
layout: post
title: '新文章标题'
date: 2024-08-26 16:00:00 +0800
categories: [Technical]
tags: [mTNT, AI]
author: 深圳王哥
---

# 新文章内容

这里是文章内容...

---

# New Article Content

Here is the article content...
" > _posts/2024-08-26-new-article.md

# 2. 检查规范
python3 scripts/check_and_deploy.py -c

# 3. 如果检查通过，部署
python3 scripts/check_and_deploy.py
```

### 场景2: 批量检查所有文件

```bash
# 检查所有文件并生成报告
python3 scripts/check_and_deploy.py -c > check_report.txt 2>&1

# 查看检查结果
cat check_report.txt
```

### 场景3: 自动化部署

```bash
# 创建自动化脚本
cat > auto_deploy.sh << 'EOF'
#!/bin/bash
cd /path/to/mTNT-aios
python3 scripts/check_and_deploy.py -c && python3 scripts/check_and_deploy.py -d
EOF

chmod +x auto_deploy.sh
./auto_deploy.sh
```

## 检查结果解读

### 成功示例
```
[SUCCESS] 文件存在: _config.yml
[SUCCESS] front matter检查通过: index.md
[SUCCESS] 双语内容检查通过: index.md
[SUCCESS] Markdown语法检查通过: index.md
[SUCCESS] 文章命名规范: 2024-08-26-article.md
```

### 警告示例
```
[WARNING] 文件缺少layout字段: _posts/article.md
[WARNING] 建议添加双语内容: _guides/guide.md
[WARNING] Jekyll未安装，跳过构建检查
```

### 错误示例
```
[ERROR] 文件不存在: _config.yml
[ERROR] 文章命名不规范: article.md (应为: YYYY-MM-DD-title.md)
[ERROR] 未闭合的代码块: _posts/article.md
```

## 常见问题解决

### 问题1: Python依赖缺失
```bash
# 安装依赖
pip3 install pyyaml

# 或使用conda
conda install pyyaml
```

### 问题2: 权限问题
```bash
# 给脚本执行权限
chmod +x scripts/check_and_deploy.sh
chmod +x scripts/check_and_deploy.py
```

### 问题3: 路径问题
```bash
# 确保在项目根目录运行
cd /path/to/mTNT-aios
python3 scripts/check_and_deploy.py -c
```

### 问题4: Git配置问题
```bash
# 检查Git配置
git config --list | grep user

# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 高级用法

### 自定义检查规则

编辑 `scripts/check_and_deploy.py` 添加自定义检查：

```python
def check_custom_rule(self, file_path: str) -> bool:
    """自定义检查规则"""
    # 添加你的检查逻辑
    return True
```

### 集成到编辑器

在VS Code中创建任务：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Check Blog",
            "type": "shell",
            "command": "python3",
            "args": ["scripts/check_and_deploy.py", "-c"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

### 定时检查

使用cron设置定时检查：

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天上午9点检查）
0 9 * * * cd /path/to/mTNT-aios && python3 scripts/check_and_deploy.py -c
```

## 最佳实践

1. **定期检查**: 每次修改后都运行检查
2. **使用Python版本**: 功能更全面，错误处理更好
3. **查看警告**: 及时修复警告，保持代码质量
4. **备份重要文件**: 部署前备份重要内容
5. **测试部署**: 在测试环境验证后再部署到生产环境

## 联系支持

如果遇到问题，请：

1. 查看 `scripts/README.md` 获取详细文档
2. 在GitHub Issues中报告问题
3. 联系项目维护者获取帮助
