#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
mTNT Blog 规范检查和自动部署脚本 (Python版本)
作者: 深圳王哥
版本: 1.0.0
"""

import os
import sys
import re
import yaml
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 颜色定义
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class BlogChecker:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def log_info(self, message: str):
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")
        
    def log_success(self, message: str):
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")
        self.success_count += 1
        
    def log_warning(self, message: str):
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")
        self.warnings.append(message)
        
    def log_error(self, message: str):
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")
        self.errors.append(message)
        
    def check_file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        full_path = self.project_root / file_path
        if not full_path.exists():
            self.log_error(f"文件不存在: {file_path}")
            return False
        self.log_success(f"文件存在: {file_path}")
        return True
        
    def check_front_matter(self, file_path: str) -> bool:
        """检查front matter格式"""
        full_path = self.project_root / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否有front matter
            if not content.startswith('---'):
                self.log_error(f"文件缺少front matter: {file_path}")
                return False
                
            # 提取front matter
            lines = content.split('\n')
            if len(lines) < 2:
                self.log_error(f"front matter格式错误: {file_path}")
                return False
                
            # 找到front matter结束位置
            end_index = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_index = i
                    break
                    
            if end_index == -1:
                self.log_error(f"front matter未正确结束: {file_path}")
                return False
                
            # 解析YAML
            front_matter_text = '\n'.join(lines[1:end_index])
            try:
                front_matter = yaml.safe_load(front_matter_text)
            except yaml.YAMLError as e:
                self.log_error(f"front matter YAML格式错误: {file_path} - {e}")
                return False
                
            # 检查必要字段
            required_fields = ['title', 'layout']
            for field in required_fields:
                if field not in front_matter:
                    self.log_warning(f"文件缺少{field}字段: {file_path}")
                    
            self.log_success(f"front matter检查通过: {file_path}")
            return True
            
        except Exception as e:
            self.log_error(f"检查front matter时出错: {file_path} - {e}")
            return False
            
    def check_bilingual_content(self, file_path: str) -> bool:
        """检查双语内容"""
        full_path = self.project_root / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 统计中文字符
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
            # 统计英文字符
            english_chars = len(re.findall(r'[a-zA-Z]', content))
            
            has_chinese = chinese_chars > 0
            has_english = english_chars > 0
            
            if not has_chinese:
                self.log_warning(f"文件缺少中文内容: {file_path}")
                
            if not has_english:
                self.log_warning(f"文件缺少英文内容: {file_path}")
                
            if has_chinese and has_english:
                self.log_success(f"双语内容检查通过: {file_path}")
                return True
            else:
                self.log_warning(f"建议添加双语内容: {file_path}")
                return False
                
        except Exception as e:
            self.log_error(f"检查双语内容时出错: {file_path} - {e}")
            return False
            
    def check_markdown_syntax(self, file_path: str) -> bool:
        """检查Markdown语法"""
        full_path = self.project_root / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            errors = 0
            
            # 检查代码块
            code_blocks = len(re.findall(r'```', content))
            if code_blocks % 2 != 0:
                self.log_error(f"未闭合的代码块: {file_path}")
                errors += 1
                
            # 检查链接
            open_brackets = len(re.findall(r'\[', content))
            close_brackets = len(re.findall(r'\]', content))
            if open_brackets != close_brackets:
                self.log_warning(f"可能有不匹配的方括号: {file_path}")
                
            # 检查图片链接
            image_links = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
            for alt_text, url in image_links:
                if not url.startswith(('http://', 'https://', '/', './')):
                    self.log_warning(f"图片链接可能有问题: {file_path} - {url}")
                    
            if errors == 0:
                self.log_success(f"Markdown语法检查通过: {file_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.log_error(f"检查Markdown语法时出错: {file_path} - {e}")
            return False
            
    def check_post_naming(self, file_path: str) -> bool:
        """检查文章命名规范"""
        filename = Path(file_path).name
        
        # 检查命名规范: YYYY-MM-DD-title.md
        pattern = r'^\d{4}-\d{2}-\d{2}-.*\.md$'
        if re.match(pattern, filename):
            self.log_success(f"文章命名规范: {filename}")
            return True
        else:
            self.log_error(f"文章命名不规范: {filename} (应为: YYYY-MM-DD-title.md)")
            return False
            
    def check_jekyll_build(self) -> bool:
        """检查Jekyll构建"""
        self.log_info("检查Jekyll构建...")
        
        try:
            # 检查Jekyll是否安装
            result = subprocess.run(['jekyll', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.log_warning("Jekyll未安装，跳过构建检查")
                return True
                
            # 尝试构建
            result = subprocess.run(['jekyll', 'build', '--safe', '--quiet'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                self.log_success("Jekyll构建成功")
                return True
            else:
                self.log_error(f"Jekyll构建失败: {result.stderr}")
                return False
                
        except FileNotFoundError:
            self.log_warning("Jekyll未安装，跳过构建检查")
            return True
        except Exception as e:
            self.log_error(f"检查Jekyll构建时出错: {e}")
            return False
            
    def check_git_status(self) -> bool:
        """检查Git状态"""
        self.log_info("检查Git状态...")
        
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.stdout.strip():
                self.log_info("发现未提交的更改")
                return True
            else:
                self.log_warning("没有未提交的更改")
                return False
                
        except Exception as e:
            self.log_error(f"检查Git状态时出错: {e}")
            return False
            
    def perform_checks(self) -> bool:
        """执行所有检查"""
        self.log_info("开始检查blog规范...")
        
        # 检查配置文件
        self.log_info("检查配置文件...")
        if not self.check_file_exists("_config.yml"):
            return False
            
        # 检查主要页面
        self.log_info("检查主要页面...")
        main_pages = ["index.md", "about.md"]
        for page in main_pages:
            if self.check_file_exists(page):
                self.check_front_matter(page)
                self.check_bilingual_content(page)
                self.check_markdown_syntax(page)
            else:
                return False
                
        # 检查文章
        self.log_info("检查文章...")
        posts_dir = self.project_root / "_posts"
        if posts_dir.exists():
            for post_file in posts_dir.glob("*.md"):
                if self.check_post_naming(str(post_file.relative_to(self.project_root))):
                    self.check_front_matter(str(post_file.relative_to(self.project_root)))
                    self.check_bilingual_content(str(post_file.relative_to(self.project_root)))
                    self.check_markdown_syntax(str(post_file.relative_to(self.project_root)))
                    
        # 检查指南和问题页面
        self.log_info("检查指南和问题页面...")
        for dir_name in ["_guides", "_issues"]:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                for file_path in dir_path.glob("*.md"):
                    relative_path = str(file_path.relative_to(self.project_root))
                    self.check_front_matter(relative_path)
                    self.check_bilingual_content(relative_path)
                    self.check_markdown_syntax(relative_path)
                    
        # 检查Jekyll构建
        if not self.check_jekyll_build():
            return False
            
        # 检查Git状态
        if not self.check_git_status():
            return False
            
        return len(self.errors) == 0
        
    def deploy(self) -> bool:
        """部署到远程仓库"""
        self.log_info("开始部署...")
        
        try:
            # 获取当前分支
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            current_branch = result.stdout.strip()
            self.log_info(f"当前分支: {current_branch}")
            
            # 添加所有更改
            subprocess.run(['git', 'add', '.'], check=True, cwd=self.project_root)
            
            # 获取更改的文件列表
            result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            changed_files = result.stdout.strip().split('\n')
            
            self.log_info("更改的文件:")
            for file in changed_files:
                if file:
                    self.log_info(f"  - {file}")
                    
            # 提交更改
            commit_message = f"feat: 自动更新blog内容 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], 
                          check=True, cwd=self.project_root)
            self.log_success(f"提交成功: {commit_message}")
            
            # 推送到远程仓库
            subprocess.run(['git', 'push', 'origin', current_branch], 
                          check=True, cwd=self.project_root)
            self.log_success(f"推送成功到 {current_branch} 分支")
            
            self.log_success("部署完成！")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log_error(f"部署失败: {e}")
            return False
        except Exception as e:
            self.log_error(f"部署时出错: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="mTNT Blog 规范检查和自动部署脚本")
    parser.add_argument('-c', '--check', action='store_true', 
                       help='仅执行检查，不部署')
    parser.add_argument('-d', '--deploy', action='store_true', 
                       help='仅执行部署，跳过检查')
    parser.add_argument('-p', '--path', default='.', 
                       help='项目根目录路径 (默认: 当前目录)')
    
    args = parser.parse_args()
    
    print(f"{Colors.BLUE}=== mTNT Blog 规范检查和自动部署脚本 ==={Colors.NC}")
    print(f"{Colors.BLUE}开始时间: {datetime.now()}{Colors.NC}")
    
    checker = BlogChecker(args.path)
    
    # 检查是否在正确的目录
    if not (checker.project_root / "_config.yml").exists():
        print(f"{Colors.RED}[ERROR] 请在mTNT-aios项目根目录运行此脚本{Colors.NC}")
        sys.exit(1)
        
    if args.deploy:
        # 仅部署模式
        print(f"{Colors.BLUE}[INFO] 仅执行部署模式...{Colors.NC}")
        if checker.deploy():
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.check:
        # 仅检查模式
        print(f"{Colors.BLUE}[INFO] 仅执行检查模式...{Colors.NC}")
        if checker.perform_checks():
            print(f"{Colors.GREEN}[SUCCESS] 所有检查通过！{Colors.NC}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[ERROR] 检查未通过，请修复问题后重试{Colors.NC}")
            sys.exit(1)
    else:
        # 完整模式
        if checker.perform_checks():
            print(f"{Colors.GREEN}[SUCCESS] 所有检查通过！{Colors.NC}")
            
            # 询问是否部署
            response = input("是否要部署到远程仓库？(y/N): ").strip().lower()
            if response in ['y', 'yes']:
                checker.deploy()
            else:
                print(f"{Colors.BLUE}[INFO] 取消部署{Colors.NC}")
        else:
            print(f"{Colors.RED}[ERROR] 检查未通过，请修复问题后重试{Colors.NC}")
            sys.exit(1)
            
    print(f"{Colors.BLUE}结束时间: {datetime.now()}{Colors.NC}")

if __name__ == "__main__":
    main()
