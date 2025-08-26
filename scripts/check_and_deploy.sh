#!/bin/bash

# mTNT Blog 规范检查和自动部署脚本
# 作者: 深圳王哥
# 版本: 1.0.0

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查函数
check_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        log_error "文件不存在: $file"
        return 1
    fi
    log_success "文件存在: $file"
    return 0
}

check_front_matter() {
    local file="$1"
    local has_front_matter=false
    
    # 检查是否有front matter
    if head -n 10 "$file" | grep -q "^---$"; then
        has_front_matter=true
    fi
    
    if [[ "$has_front_matter" == "false" ]]; then
        log_error "文件缺少front matter: $file"
        return 1
    fi
    
    # 检查必要的front matter字段
    local required_fields=("title" "layout")
    for field in "${required_fields[@]}"; do
        if ! grep -q "^$field:" "$file"; then
            log_warning "文件缺少$field字段: $file"
        fi
    done
    
    log_success "front matter检查通过: $file"
    return 0
}

check_bilingual_content() {
    local file="$1"
    local chinese_count=$(grep -o '[一-龯]' "$file" | wc -l)
    local english_count=$(grep -o '[a-zA-Z]' "$file" | wc -l)
    
    # 检查是否有中英文内容
    if [[ $chinese_count -eq 0 ]]; then
        log_warning "文件缺少中文内容: $file"
    fi
    
    if [[ $english_count -eq 0 ]]; then
        log_warning "文件缺少英文内容: $file"
    fi
    
    # 检查中英文比例（简单检查）
    if [[ $chinese_count -gt 0 && $english_count -gt 0 ]]; then
        log_success "双语内容检查通过: $file"
    else
        log_warning "建议添加双语内容: $file"
    fi
}

check_markdown_syntax() {
    local file="$1"
    local errors=0
    
    # 检查markdown语法
    # 检查是否有未闭合的代码块
    local code_blocks=$(grep -c '```' "$file" || echo 0)
    if [[ $((code_blocks % 2)) -ne 0 ]]; then
        log_error "未闭合的代码块: $file"
        ((errors++))
    fi
    
    # 检查是否有未闭合的链接
    local open_brackets=$(grep -o '\[' "$file" | wc -l)
    local close_brackets=$(grep -o '\]' "$file" | wc -l)
    if [[ $open_brackets -ne $close_brackets ]]; then
        log_warning "可能有不匹配的方括号: $file"
    fi
    
    if [[ $errors -eq 0 ]]; then
        log_success "Markdown语法检查通过: $file"
    fi
    
    return $errors
}

check_post_naming() {
    local file="$1"
    local filename=$(basename "$file")
    
    # 检查文章命名规范 (YYYY-MM-DD-title.md)
    if [[ "$filename" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-.*\.md$ ]]; then
        log_success "文章命名规范: $filename"
        return 0
    else
        log_error "文章命名不规范: $filename (应为: YYYY-MM-DD-title.md)"
        return 1
    fi
}

check_jekyll_build() {
    log_info "检查Jekyll构建..."
    
    # 检查是否有Jekyll
    if ! command -v jekyll &> /dev/null; then
        log_warning "Jekyll未安装，跳过构建检查"
        return 0
    fi
    
    # 尝试构建
    if jekyll build --safe --quiet; then
        log_success "Jekyll构建成功"
        return 0
    else
        log_error "Jekyll构建失败"
        return 1
    fi
}

check_git_status() {
    log_info "检查Git状态..."
    
    # 检查是否有未提交的更改
    if [[ -n $(git status --porcelain) ]]; then
        log_info "发现未提交的更改"
        return 0
    else
        log_warning "没有未提交的更改"
        return 1
    fi
}

# 主检查函数
perform_checks() {
    local errors=0
    local warnings=0
    
    log_info "开始检查blog规范..."
    
    # 检查配置文件
    log_info "检查配置文件..."
    if ! check_file_exists "_config.yml"; then
        ((errors++))
    fi
    
    # 检查主要页面
    log_info "检查主要页面..."
    local main_pages=("index.md" "about.md")
    for page in "${main_pages[@]}"; do
        if check_file_exists "$page"; then
            check_front_matter "$page"
            check_bilingual_content "$page"
            check_markdown_syntax "$page"
        else
            ((errors++))
        fi
    done
    
    # 检查文章
    log_info "检查文章..."
    for post in _posts/*.md; do
        if [[ -f "$post" ]]; then
            if check_post_naming "$post"; then
                check_front_matter "$post"
                check_bilingual_content "$post"
                check_markdown_syntax "$post"
            else
                ((errors++))
            fi
        fi
    done
    
    # 检查指南和问题页面
    log_info "检查指南和问题页面..."
    for guide in _guides/*.md; do
        if [[ -f "$guide" ]]; then
            check_front_matter "$guide"
            check_bilingual_content "$guide"
            check_markdown_syntax "$guide"
        fi
    done
    
    for issue in _issues/*.md; do
        if [[ -f "$issue" ]]; then
            check_front_matter "$issue"
            check_bilingual_content "$issue"
            check_markdown_syntax "$issue"
        fi
    done
    
    # 检查Jekyll构建
    check_jekyll_build || ((errors++))
    
    # 检查Git状态
    if check_git_status; then
        log_info "准备部署..."
    else
        log_warning "没有需要部署的更改"
        return 1
    fi
    
    return $errors
}

# 部署函数
deploy() {
    log_info "开始部署..."
    
    # 获取当前分支
    local current_branch=$(git branch --show-current)
    log_info "当前分支: $current_branch"
    
    # 添加所有更改
    git add .
    
    # 获取更改的文件列表
    local changed_files=$(git diff --cached --name-only)
    log_info "更改的文件:"
    echo "$changed_files" | while read -r file; do
        if [[ -n "$file" ]]; then
            log_info "  - $file"
        fi
    done
    
    # 提交更改
    local commit_message="feat: 自动更新blog内容 - $(date '+%Y-%m-%d %H:%M:%S')"
    if git commit -m "$commit_message"; then
        log_success "提交成功: $commit_message"
    else
        log_error "提交失败"
        return 1
    fi
    
    # 推送到远程仓库
    if git push origin "$current_branch"; then
        log_success "推送成功到 $current_branch 分支"
    else
        log_error "推送失败"
        return 1
    fi
    
    log_success "部署完成！"
    return 0
}

# 主函数
main() {
    log_info "=== mTNT Blog 规范检查和自动部署脚本 ==="
    log_info "开始时间: $(date)"
    
    # 检查是否在正确的目录
    if [[ ! -f "_config.yml" ]]; then
        log_error "请在mTNT-aios项目根目录运行此脚本"
        exit 1
    fi
    
    # 执行检查
    if perform_checks; then
        log_success "所有检查通过！"
        
        # 询问是否部署
        read -p "是否要部署到远程仓库？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            deploy
        else
            log_info "取消部署"
        fi
    else
        log_error "检查未通过，请修复问题后重试"
        exit 1
    fi
    
    log_info "结束时间: $(date)"
}

# 帮助函数
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -c, --check    仅执行检查，不部署"
    echo "  -d, --deploy   仅执行部署，跳过检查"
    echo ""
    echo "示例:"
    echo "  $0             执行完整检查和部署"
    echo "  $0 -c          仅检查规范"
    echo "  $0 -d          仅部署（跳过检查）"
}

# 参数处理
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -c|--check)
        log_info "仅执行检查模式..."
        perform_checks
        exit $?
        ;;
    -d|--deploy)
        log_info "仅执行部署模式..."
        deploy
        exit $?
        ;;
    "")
        main
        ;;
    *)
        log_error "未知选项: $1"
        show_help
        exit 1
        ;;
esac
