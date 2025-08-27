// mTNT Blog - 移动端优化 JavaScript

// 检测移动设备
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// 检测触摸设备
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// 移动端优化
if (isMobile() || isTouchDevice()) {
    // 防止双击缩放
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);

    // 优化滚动性能
    document.addEventListener('touchmove', function (event) {
        if (event.scale !== 1) {
            event.preventDefault();
        }
    }, { passive: false });

    // 添加移动端类名
    document.body.classList.add('mobile-device');
}

// 响应式导航菜单
function initMobileNav() {
    const nav = document.querySelector('nav ul');
    if (!nav) return;

    // 创建移动端菜单按钮
    const menuButton = document.createElement('button');
    menuButton.className = 'mobile-menu-btn';
    menuButton.innerHTML = '☰';
    menuButton.setAttribute('aria-label', 'Toggle navigation menu');

    // 插入菜单按钮到header-content中
    const headerContent = document.querySelector('.header-content');
    if (headerContent) {
        headerContent.appendChild(menuButton);
    }

    // 切换菜单显示
    menuButton.addEventListener('click', function(e) {
        e.stopPropagation(); // 阻止事件冒泡
        nav.classList.toggle('nav-open');
        menuButton.classList.toggle('active');
    });

    // 点击外部关闭菜单
    document.addEventListener('click', function(event) {
        if (!headerContent.contains(event.target)) {
            nav.classList.remove('nav-open');
            menuButton.classList.remove('active');
        }
    });

    // 点击菜单项后关闭菜单
    nav.addEventListener('click', function(event) {
        if (event.target.tagName === 'A') {
            nav.classList.remove('nav-open');
            menuButton.classList.remove('active');
        }
    });
}

// 图片懒加载
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // 降级处理
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// 代码块优化
function initCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        // 添加复制按钮
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.textContent = '复制';
        copyButton.setAttribute('aria-label', 'Copy code to clipboard');
        
        copyButton.addEventListener('click', async function() {
            try {
                await navigator.clipboard.writeText(block.textContent);
                copyButton.textContent = '已复制!';
                setTimeout(() => {
                    copyButton.textContent = '复制';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy code:', err);
                copyButton.textContent = '复制失败';
            }
        });
        
        block.parentElement.appendChild(copyButton);
    });
}

// 平滑滚动
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initMobileNav();
    initLazyLoading();
    initCodeBlocks();
    initSmoothScroll();
    
    // 添加页面加载动画
    document.body.classList.add('loaded');
});

// 性能监控
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('页面加载时间:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}