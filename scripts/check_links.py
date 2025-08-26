#!/usr/bin/env python3
"""
链接检查脚本 - 检查博客中的所有链接
Link Checker Script - Check all links in the blog
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path

class LinkChecker:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.internal_links = []
        self.external_links = []
        self.broken_links = []
        self.checked_files = []
        
    def find_all_files(self):
        """查找所有需要检查的文件"""
        extensions = ['.html', '.md', '.yml']
        files = []
        
        for ext in extensions:
            files.extend(self.root_dir.rglob(f'*{ext}'))
        
        # 排除一些不需要检查的文件
        exclude_patterns = ['.git', '.dist', 'node_modules', '__pycache__']
        filtered_files = []
        
        for file in files:
            if not any(pattern in str(file) for pattern in exclude_patterns):
                filtered_files.append(file)
        
        return filtered_files
    
    def extract_links_from_file(self, file_path):
        """从文件中提取链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            return []
        
        links = []
        
        # 查找各种类型的链接
        patterns = [
            r'href=["\']([^"\']+)["\']',  # HTML href
            r'src=["\']([^"\']+)["\']',   # HTML src
            r'\[([^\]]+)\]\(([^)]+)\)',   # Markdown links
            r'url:\s*["\']([^"\']+)["\']', # YAML url
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    # Markdown link
                    link = match[1]
                else:
                    # HTML/YAML link
                    link = match
                
                if link and not link.startswith('#'):
                    links.append({
                        'url': link,
                        'file': str(file_path),
                        'line': self.find_line_number(content, link)
                    })
        
        return links
    
    def find_line_number(self, content, link):
        """查找链接在文件中的行号"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if link in line:
                return i
        return 0
    
    def is_internal_link(self, url):
        """判断是否为内部链接"""
        if url.startswith('http'):
            return False
        if url.startswith('mailto:'):
            return False
        if url.startswith('#'):
            return False
        return True
    
    def check_internal_link(self, url, base_file):
        """检查内部链接"""
        if url.startswith('/'):
            # 绝对路径
            target_path = self.root_dir / url.lstrip('/')
        else:
            # 相对路径
            base_dir = Path(base_file).parent
            target_path = base_dir / url
        
        # 处理Jekyll模板语法
        if '{{' in str(target_path) or '}}' in str(target_path):
            return True  # 跳过模板语法
        
        # 检查文件是否存在
        if target_path.exists():
            return True
        
        # 检查是否有对应的.html文件
        if not target_path.suffix:
            html_path = target_path.with_suffix('.html')
            if html_path.exists():
                return True
        
        return False
    
    def check_external_link(self, url):
        """检查外部链接"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
        except Exception:
            return False
    
    def check_all_links(self):
        """检查所有链接"""
        files = self.find_all_files()
        
        for file_path in files:
            print(f"检查文件: {file_path}")
            links = self.extract_links_from_file(file_path)
            
            for link_info in links:
                url = link_info['url']
                
                if self.is_internal_link(url):
                    self.internal_links.append(link_info)
                    if not self.check_internal_link(url, link_info['file']):
                        self.broken_links.append({
                            **link_info,
                            'type': 'internal'
                        })
                else:
                    self.external_links.append(link_info)
                    if not self.check_external_link(url):
                        self.broken_links.append({
                            **link_info,
                            'type': 'external'
                        })
    
    def generate_report(self):
        """生成检查报告"""
        report = []
        report.append("# 链接检查报告 / Link Check Report")
        report.append("")
        
        # 统计信息
        report.append("## 统计信息 / Statistics")
        report.append(f"- 内部链接总数: {len(self.internal_links)}")
        report.append(f"- 外部链接总数: {len(self.external_links)}")
        report.append(f"- 损坏链接数: {len(self.broken_links)}")
        report.append("")
        
        # 损坏的链接
        if self.broken_links:
            report.append("## 损坏的链接 / Broken Links")
            report.append("")
            
            for link in self.broken_links:
                report.append(f"### {link['file']}:{link['line']}")
                report.append(f"- URL: `{link['url']}`")
                report.append(f"- 类型: {link['type']}")
                report.append("")
        else:
            report.append("## 损坏的链接 / Broken Links")
            report.append("✅ 没有发现损坏的链接！")
            report.append("")
        
        # 内部链接列表
        report.append("## 内部链接 / Internal Links")
        report.append("")
        for link in self.internal_links:
            report.append(f"- `{link['url']}` (在 {link['file']}:{link['line']})")
        report.append("")
        
        # 外部链接列表
        report.append("## 外部链接 / External Links")
        report.append("")
        for link in self.external_links:
            report.append(f"- `{link['url']}` (在 {link['file']}:{link['line']})")
        
        return "\n".join(report)

def main():
    checker = LinkChecker()
    print("开始检查链接...")
    checker.check_all_links()
    
    report = checker.generate_report()
    
    # 保存报告
    with open('link_check_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("链接检查完成！报告已保存到 link_check_report.md")
    print(f"发现 {len(checker.broken_links)} 个损坏的链接")

if __name__ == "__main__":
    main()
