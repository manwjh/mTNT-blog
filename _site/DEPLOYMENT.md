# mTNT Blog 部署指南

本文档介绍如何将mTNT Blog部署到各种平台。

## 🚀 GitHub Pages 部署

### 方法1: 使用GitHub Actions（推荐）

1. **创建GitHub仓库**
   ```bash
   # 在GitHub上创建新仓库: manwjh/mTNT-blog
   ```

2. **推送代码**
   ```bash
   git remote add origin https://github.com/manwjh/mTNT-blog.git
   git branch -M main
   git push -u origin main
   ```

3. **创建GitHub Actions工作流**
   
   创建文件 `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       
       steps:
       - name: Checkout
         uses: actions/checkout@v3
   
       - name: Set up Ruby
         uses: ruby/setup-ruby@v1
         with:
           ruby-version: '3.0'
           bundler-cache: true
   
       - name: Install dependencies
         run: |
           bundle install
   
       - name: Build site
         run: |
           bundle exec jekyll build
   
       - name: Deploy to GitHub Pages
         if: github.ref == 'refs/heads/main'
         uses: peaceiris/actions-gh-pages@v3
         with:
           github_token: ${{ secrets.GITHUB_TOKEN }}
           publish_dir: ./_site
   ```

4. **启用GitHub Pages**
   - 进入仓库设置 → Pages
   - Source选择 "Deploy from a branch"
   - Branch选择 "gh-pages"
   - 保存设置

### 方法2: 手动部署

1. **构建网站**
   ```bash
   bundle install
   bundle exec jekyll build
   ```

2. **推送到gh-pages分支**
   ```bash
   git checkout -b gh-pages
   git add _site -f
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

## 🌐 Netlify 部署

1. **连接GitHub仓库**
   - 登录 [Netlify](https://netlify.com)
   - 点击 "New site from Git"
   - 选择GitHub，授权访问仓库

2. **配置构建设置**
   ```
   Build command: bundle exec jekyll build
   Publish directory: _site
   ```

3. **环境变量设置**
   ```
   JEKYLL_ENV: production
   ```

4. **部署**
   - 点击 "Deploy site"
   - 等待构建完成

## ⚡ Vercel 部署

1. **连接GitHub仓库**
   - 登录 [Vercel](https://vercel.com)
   - 点击 "New Project"
   - 导入GitHub仓库

2. **配置构建设置**
   ```
   Framework Preset: Other
   Build Command: bundle exec jekyll build
   Output Directory: _site
   ```

3. **部署**
   - 点击 "Deploy"
   - 等待构建完成

## ☁️ 阿里云OSS部署

1. **安装阿里云CLI**
   ```bash
   pip install aliyun-cli
   ```

2. **配置认证**
   ```bash
   aliyun configure
   ```

3. **创建部署脚本**
   ```bash
   #!/bin/bash
   bundle exec jekyll build
   aliyun oss cp _site/ oss://your-bucket-name/ --recursive
   ```

## 🐳 Docker 部署

1. **创建Dockerfile**
   ```dockerfile
   FROM ruby:3.0-alpine
   
   WORKDIR /app
   
   COPY Gemfile Gemfile.lock ./
   RUN bundle install
   
   COPY . .
   RUN bundle exec jekyll build
   
   FROM nginx:alpine
   COPY --from=0 /app/_site /usr/share/nginx/html
   
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **构建和运行**
   ```bash
   docker build -t mtnt-blog .
   docker run -p 80:80 mtnt-blog
   ```

## 🔧 本地开发

### 环境要求

- Ruby 2.7+
- Jekyll 4.0+
- Bundler

### 安装步骤

1. **安装Ruby**
   ```bash
   # macOS (使用Homebrew)
   brew install ruby
   
   # Ubuntu/Debian
   sudo apt-get install ruby-full
   
   # CentOS/RHEL
   sudo yum install ruby
   ```

2. **安装Jekyll**
   ```bash
   gem install jekyll bundler
   ```

3. **启动开发服务器**
   ```bash
   bundle install
   bundle exec jekyll serve
   ```

4. **访问网站**
   打开浏览器访问: http://localhost:4000

## 📝 自定义域名

### GitHub Pages

1. **添加CNAME文件**
   ```
   your-domain.com
   ```

2. **配置DNS**
   ```
   CNAME your-domain.com manwjh.github.io
   ```

### Netlify

1. **添加自定义域名**
   - 进入站点设置 → Domain management
   - 点击 "Add custom domain"
   - 输入域名

2. **配置DNS**
   ```
   CNAME your-domain.com your-site.netlify.app
   ```

## 🔒 HTTPS配置

### GitHub Pages
- 自动启用HTTPS
- 在仓库设置中勾选 "Enforce HTTPS"

### Netlify
- 自动启用HTTPS
- 支持Let's Encrypt证书

### 其他平台
- 配置SSL证书
- 重定向HTTP到HTTPS

## 📊 性能优化

### 图片优化
```bash
# 使用ImageOptim压缩图片
# 或使用在线工具如TinyPNG
```

### CSS/JS优化
```bash
# 压缩CSS
bundle exec jekyll build --incremental

# 使用CDN
# 在_config.yml中配置CDN链接
```

### 缓存策略
```yaml
# 在_config.yml中添加缓存头
headers:
  - scope: assets
    values:
      Cache-Control: "public, max-age=31536000"
```

## 🚨 故障排除

### 常见问题

1. **构建失败**
   ```bash
   # 检查Ruby版本
   ruby --version
   
   # 更新依赖
   bundle update
   
   # 清理缓存
   bundle exec jekyll clean
   ```

2. **样式不显示**
   - 检查CSS文件路径
   - 确认baseurl配置正确
   - 检查GitHub Pages设置

3. **图片不显示**
   - 检查图片路径
   - 确认图片文件存在
   - 检查文件权限

### 调试技巧

```bash
# 详细构建日志
bundle exec jekyll build --verbose

# 本地调试
bundle exec jekyll serve --incremental --drafts

# 检查语法
bundle exec jekyll doctor
```

## 📞 支持

如果遇到部署问题，请：

1. 查看 [Jekyll官方文档](https://jekyllrb.com/docs/)
2. 检查 [GitHub Pages文档](https://pages.github.com/)
3. 在GitHub Issues中报告问题
4. 联系项目维护者

---

**祝您部署顺利！** 🚀
