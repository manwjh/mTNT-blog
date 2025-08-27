source "https://rubygems.org"

# 指定Ruby版本要求
ruby "~> 2.6.0"

# 注意: 不要在这里指定bundler版本，会与系统bundler冲突

# GitHub Pages 和 Jekyll
gem "github-pages", "~> 228", group: :jekyll_plugins

# 插件
group :jekyll_plugins do
  # 使用GitHub Pages原生支持的插件
  gem "jekyll-paginate"
end

# Windows 和 JRuby 兼容性
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1"
  gem "tzinfo-data"
end

# 性能优化
gem "wdm", ">= 0.1.0", :platforms => [:mingw, :x64_mingw, :mswin]
gem "webrick", "~> 1.7"

# 兼容性修复
gem "ffi", "~> 1.15.0"
