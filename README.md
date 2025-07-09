# Jesse Project Template

#jess文档 请参阅：
https://docs.jesse.trade/docs/getting-started/

其他jesse教程文档在docs目录下，但不包括docs目录的各个子目录，docs目录的各个子目录是运行时的文档

## 📋 开发规范

请查看 [CODING_STANDARDS.md](./CODING_STANDARDS.md) 了解详细的编码规范，包括：
- 注释语言规范（策略文件使用英文，其他文件使用中文）
Jesse AI 交易机器人项目
这是一个基于 Jesse 框架的算法交易机器人项目 - Jesse 是一个用 Python 开发的高级算法交易框架，专门用于开发和回测交易策略。

📊 项目概况
主要用途：

开发自动化加密货币/金融交易策略
使用历史数据回测策略
部署实时交易机器人
技术栈：

Jesse 框架 - 先进的交易框架
Python >= 3.10（配合 PostgreSQL 和 Redis）
--Docker 支持便捷部署(待后期实现)
PostgreSQL 用于数据存储
Redis 用于缓存
🚀 当前交易策略
项目包含 6 种不同的交易策略：

BuyHold - 激进的买入持有策略（30 天内每 3 天买入一次）
moveAverage - 基于移动平均线的策略
RSIStrategy - RSI 均值回归策略（超卖/超买水平）
SmartHold - 智能持有策略
TestStrategy - 测试/实验性策略
trendstrate - 趋势跟踪策略
📁 关键组件
strategies - 包含所有交易策略实现
storage - 日志、回测结果和数据存储
docs - 完整的文档（设置、指南、API 密钥）
docker - Docker 部署配置
sqls - 数据库测试和 PostgreSQL 工具
🎯 开发规范
项目遵循严格的编码标准：

策略文件：仅使用英文注释
其他文件：优先使用中文注释
所有策略都有完整的文档
📈 数据与回测
历史数据存储在 temp（来自币安的比特币/USDT数据）,并且保存在PostgreSQL数据库
回测结果和分析存储在 storage
支持 TradingView 导出功能
有性能对比文档
这是一个生产级的算法交易系统，专为加密货币市场设计，具有多种策略、完善的测试能力和专业的部署基础设施。

🔄 项目当前状态