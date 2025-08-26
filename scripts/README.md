# mTNT Blog 规范检查和自动部署脚本

这个目录包含了用于检查和部署mTNT Blog的自动化脚本。

## 脚本说明

### 1. `check_and_deploy.sh` (Bash版本)
- **功能**: 检查blog编写规范并自动部署
- **特点**: 轻量级，依赖少，适合快速检查
- **要求**: Bash环境

### 2. `check_and_deploy.py` (Python版本)
- **功能**: 更强大的规范检查和自动部署
- **特点**: 功能更全面，错误处理更好，支持更多检查项
- **要求**: Python 3.6+

## 检查规范

### 文件结构检查
- ✅ 检查必要文件是否存在 (`_config.yml`, `index.md`, `about.md`)
- ✅ 检查目录结构是否正确

### Front Matter检查
- ✅ 检查是否有front matter
- ✅ 检查必要字段 (`title`, `layout`)
- ✅ 检查YAML格式是否正确

### 双语内容检查
- ✅ 检查是否包含中文内容
- ✅ 检查是否包含英文内容
- ✅ 建议添加双语内容

### Markdown语法检查
- ✅ 检查代码块是否闭合
- ✅ 检查链接格式是否正确
- ✅ 检查图片链接是否有效
- ✅ 检查方括号是否匹配

### 文章命名检查
- ✅ 检查文章命名是否符合规范 (`YYYY-MM-DD-title.md`)

### Jekyll构建检查
- ✅ 检查Jekyll是否能正常构建
- ✅ 检查构建过程中是否有错误

### Git状态检查
- ✅ 检查是否有未提交的更改
- ✅ 检查当前分支状态

## 使用方法

### Bash脚本使用

```bash
# 给脚本执行权限
chmod +x scripts/check_and_deploy.sh

# 完整检查和部署
./scripts/check_and_deploy.sh

# 仅执行检查
./scripts/check_and_deploy.sh -c

# 仅执行部署
./scripts/check_and_deploy.sh -d

# 查看帮助
./scripts/check_and_deploy.sh -h
```

### Python脚本使用

```bash
# 安装依赖
pip install pyyaml

# 完整检查和部署
python scripts/check_and_deploy.py

# 仅执行检查
python scripts/check_and_deploy.py -c

# 仅执行部署
python scripts/check_and_deploy.py -d

# 指定项目路径
python scripts/check_and_deploy.py -p /path/to/project

# 查看帮助
python scripts/check_and_deploy.py -h
```

## 输出说明

### 颜色编码
- 🔵 **蓝色**: 信息提示
- 🟢 **绿色**: 成功信息
- 🟡 **黄色**: 警告信息
- 🔴 **红色**: 错误信息

### 检查结果
- ✅ **SUCCESS**: 检查通过
- ⚠️ **WARNING**: 发现问题但不影响部署
- ❌ **ERROR**: 严重问题，需要修复

## 部署流程

1. **检查阶段**
   - 验证所有文件格式和内容
   - 检查Jekyll构建
   - 确认Git状态

2. **部署阶段**
   - 添加所有更改到Git
   - 生成提交信息
   - 推送到远程仓库

3. **确认阶段**
   - 显示部署结果
   - 提供部署状态反馈

## 常见问题

### Q: 脚本报错"文件不存在"
A: 确保在mTNT-aios项目根目录运行脚本

### Q: Jekyll构建失败
A: 检查Jekyll是否正确安装，或安装Jekyll:
```bash
gem install jekyll bundler
```

### Q: Git推送失败
A: 检查网络连接和Git配置，确保有推送权限

### Q: Python脚本依赖错误
A: 安装必要的Python包:
```bash
pip install pyyaml
```

## 自定义配置

### 修改检查规则
编辑脚本中的检查函数来自定义检查规则：

```python
# 在Python脚本中修改
def check_custom_rule(self, file_path: str) -> bool:
    # 添加自定义检查逻辑
    pass
```

### 修改部署行为
编辑部署函数来自定义部署流程：

```python
# 在Python脚本中修改
def deploy(self) -> bool:
    # 添加自定义部署逻辑
    pass
```

## 自动化集成

### GitHub Actions
可以创建GitHub Actions工作流来自动运行检查：

```yaml
name: Blog Check and Deploy
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Blog Check
        run: python scripts/check_and_deploy.py -c
```

### 定时任务
可以设置cron任务定期检查：

```bash
# 每天检查一次
0 9 * * * cd /path/to/mTNT-aios && python scripts/check_and_deploy.py -c
```

## 贡献指南

欢迎提交Issue和Pull Request来改进这些脚本：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。
