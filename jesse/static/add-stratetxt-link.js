// 添加策略文档链接脚本
(function() {
    'use strict';
    
    // 等待页面加载完成
    function waitForElement(selector, callback, maxAttempts = 50) {
        let attempts = 0;
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element || attempts >= maxAttempts) {
                clearInterval(interval);
                if (element) {
                    callback(element);
                }
            }
            attempts++;
        }, 100);
    }
    
    // 添加策略文档链接
    function addStrategyDocsLinks() {
        // 避免重复添加 - 更严格的检查
        if (document.querySelector('a[href="/stratetxt"]') ||
            document.querySelector('a[href="/strategy-write"]') ||
            document.querySelector('a[href="/strategy-execute"]') ||
            document.querySelector('.strategy-docs-added')) {
            return;
        }

        // 查找导航菜单
        waitForElement('nav, .nav, .navigation, [role="navigation"]', (nav) => {
            console.log('找到导航元素:', nav);
            addLinksToNav(nav);
        });

        // 也尝试直接在页面中查找链接列表
        waitForElement('a[href*="strategies"], a[href*="import"]', (existingLink) => {
            console.log('找到现有链接:', existingLink);
            addLinksNearExisting(existingLink);
        });
    }
    
    function addLinksToNav(nav) {
        // 检查是否已经添加过
        if (nav.querySelector('a[href="/stratetxt"]') ||
            nav.querySelector('a[href="/strategy-write"]') ||
            nav.querySelector('a[href="/strategy-execute"]')) {
            return;
        }

        // 创建三个链接
        const strategyRecommendLink = createStrategyRecommendLink();
        const strategyWriteLink = createStrategyWriteLink();
        const strategyExecuteLink = createStrategyExecuteLink();

        // 尝试找到合适的位置插入
        const strategiesLink = nav.querySelector('a[href*="strategies"]');
        const importLink = nav.querySelector('a[href*="import"]');

        if (strategiesLink && importLink) {
            // 在strategies和import之间插入
            strategiesLink.parentNode.insertBefore(strategyRecommendLink, importLink);
            strategiesLink.parentNode.insertBefore(strategyWriteLink, importLink);
            strategiesLink.parentNode.insertBefore(strategyExecuteLink, importLink);
        } else if (strategiesLink) {
            // 在strategies后面插入
            strategiesLink.parentNode.insertBefore(strategyRecommendLink, strategiesLink.nextSibling);
            strategiesLink.parentNode.insertBefore(strategyWriteLink, strategiesLink.nextSibling);
            strategiesLink.parentNode.insertBefore(strategyExecuteLink, strategiesLink.nextSibling);
        } else {
            // 直接添加到导航末尾
            nav.appendChild(strategyRecommendLink);
            nav.appendChild(strategyWriteLink);
            nav.appendChild(strategyExecuteLink);
        }

        // 添加标记
        nav.classList.add('strategy-docs-added');
    }

    function addLinksNearExisting(existingLink) {
        // 避免重复添加
        if (existingLink.parentNode.querySelector('a[href="/stratetxt"]') ||
            existingLink.parentNode.querySelector('a[href="/strategy-write"]') ||
            existingLink.parentNode.querySelector('a[href="/strategy-execute"]')) {
            return;
        }

        const strategyRecommendLink = createStrategyRecommendLink();
        const strategyWriteLink = createStrategyWriteLink();
        const strategyExecuteLink = createStrategyExecuteLink();

        // 复制现有链接的样式
        strategyRecommendLink.className = existingLink.className;
        strategyWriteLink.className = existingLink.className;
        strategyExecuteLink.className = existingLink.className;

        // 在现有链接后插入
        existingLink.parentNode.insertBefore(strategyRecommendLink, existingLink.nextSibling);
        existingLink.parentNode.insertBefore(strategyWriteLink, existingLink.nextSibling);
        existingLink.parentNode.insertBefore(strategyExecuteLink, existingLink.nextSibling);
    }
    
    function createStrategyRecommendLink() {
        const link = document.createElement('a');
        link.href = '/stratetxt';
        link.target = '_blank'; // 在新标签页中打开
        link.rel = 'noopener noreferrer'; // 安全性考虑
        link.textContent = '策略推荐';
        link.title = '查看策略推荐和说明（新窗口打开）';

        // 添加一些基本样式
        link.style.cssText = `
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            margin: 0 4px;
            text-decoration: none;
            color: inherit;
            border-radius: 6px;
            transition: background-color 0.2s;
            position: relative;
        `;

        // 添加新窗口图标
        const newWindowIcon = document.createElement('span');
        newWindowIcon.innerHTML = ' ↗';
        newWindowIcon.style.cssText = `
            font-size: 12px;
            opacity: 0.7;
            margin-left: 4px;
        `;
        link.appendChild(newWindowIcon);

        // 添加悬停效果
        link.addEventListener('mouseenter', () => {
            link.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
        });

        link.addEventListener('mouseleave', () => {
            link.style.backgroundColor = 'transparent';
        });

        return link;
    }

    function createStrategyWriteLink() {
        const link = document.createElement('a');
        link.href = '/strategy-write';
        link.target = '_blank'; // 在新标签页中打开
        link.rel = 'noopener noreferrer'; // 安全性考虑
        link.textContent = '帮我编写';
        link.title = 'AI帮助编写策略（新窗口打开）';

        // 添加一些基本样式
        link.style.cssText = `
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            margin: 0 4px;
            text-decoration: none;
            color: inherit;
            border-radius: 6px;
            transition: background-color 0.2s;
            position: relative;
        `;

        // 添加新窗口图标
        const newWindowIcon = document.createElement('span');
        newWindowIcon.innerHTML = ' ↗';
        newWindowIcon.style.cssText = `
            font-size: 12px;
            opacity: 0.7;
            margin-left: 4px;
        `;
        link.appendChild(newWindowIcon);

        // 添加悬停效果
        link.addEventListener('mouseenter', () => {
            link.style.backgroundColor = 'rgba(34, 197, 94, 0.1)';
        });

        link.addEventListener('mouseleave', () => {
            link.style.backgroundColor = 'transparent';
        });

        return link;
    }

    function createStrategyExecuteLink() {
        const link = document.createElement('a');
        link.href = '/strategy-execute';
        link.target = '_blank'; // 在新标签页中打开
        link.rel = 'noopener noreferrer'; // 安全性考虑
        link.textContent = '执行策略';
        link.title = '自动化执行策略 - 支持TradingView信号和多交易所（新窗口打开）';

        // 添加一些基本样式
        link.style.cssText = `
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            margin: 0 4px;
            text-decoration: none;
            color: inherit;
            border-radius: 6px;
            transition: background-color 0.2s;
            position: relative;
        `;

        // 添加新窗口图标
        const newWindowIcon = document.createElement('span');
        newWindowIcon.innerHTML = ' ↗';
        newWindowIcon.style.cssText = `
            font-size: 12px;
            opacity: 0.7;
            margin-left: 4px;
        `;
        link.appendChild(newWindowIcon);

        // 添加悬停效果
        link.addEventListener('mouseenter', () => {
            link.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
        });

        link.addEventListener('mouseleave', () => {
            link.style.backgroundColor = 'transparent';
        });

        return link;
    }

    // 添加自定义样式
    function addCustomStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* 策略文档链接样式 */
            a[href="/stratetxt"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white !important;
                font-weight: 500;
            }
            
            a[href="/stratetxt"]:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            }
            
            a[href="/strategy-write"] {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white !important;
                font-weight: 500;
            }
            
            a[href="/strategy-write"]:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
            }

            a[href="/strategy-execute"] {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white !important;
                font-weight: 500;
            }

            a[href="/strategy-execute"]:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
            }

            /* 新窗口图标样式 */
            a[href="/stratetxt"] span,
            a[href="/strategy-write"] span,
            a[href="/strategy-execute"] span {
                transition: transform 0.2s;
            }

            a[href="/stratetxt"]:hover span,
            a[href="/strategy-write"]:hover span,
            a[href="/strategy-execute"]:hover span {
                transform: scale(1.2);
            }
        `;
        document.head.appendChild(style);
    }
    
    // 监听页面变化（适用于SPA应用）
    function observePageChanges() {
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    shouldUpdate = true;
                }
            });
            
            if (shouldUpdate) {
                setTimeout(() => {
                    addStrategyDocsLinks();
                }, 500);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // 初始化
    function init() {
        console.log('初始化策略文档链接...');
        
        // 添加自定义样式
        addCustomStyles();
        
        // 等待页面完全加载
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(runCustomizations, 1000);
            });
        } else {
            setTimeout(runCustomizations, 1000);
        }
        
        // 监听页面变化
        observePageChanges();
    }
    
    function runCustomizations() {
        addStrategyDocsLinks();

        // 定期重新应用自定义（适用于动态内容）
        setInterval(() => {
            addStrategyDocsLinks();
        }, 30000); // 进一步增加间隔避免频繁检查
    }
    
    // 启动
    init();
})();
