source "https://rubygems.org"

# GitHub Pages 和 Jekyll
gem "github-pages", group: :jekyll_plugins

# 插件
group :jekyll_plugins do
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
