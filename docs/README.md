# Jesse 交易框架文档

这是 Jesse 交易框架的中文文档，整理自官方文档：https://docs.jesse.trade/

## 文档目录

### 入门指南
- [快速开始指南](getting-started.md) - Jesse 安装与基础配置
- [环境配置](environment-setup.md) - 各操作系统环境配置详解
- [Docker 部署](docker.md) - 使用 Docker 快速部署 Jesse
- [更新升级](update.md) - Jesse 版本更新方法

### 核心功能
- [配置说明](configuration.md) - 环境变量和应用设置详解
- [策略开发](strategies.md) - 编写自定义交易策略
- [回测分析](backtest.md) - 策略回测和结果分析

### 高级主题
- [数据导入](import-candles.md) - 导入历史蜡烛图数据
- [路由配置](routes.md) - 配置交易路由
- [实盘交易](live-trading.md) - 连接交易所进行实盘交易
- [工具函数](utils.md) - Jesse 提供的工具函数
- [调试技巧](debugging.md) - 策略调试和问题排查

## 关于 Jesse

Jesse 是一个先进的加密货币算法交易框架，支持：

- 📈 **回测** - 使用历史数据测试策略
- 🤖 **实盘交易** - 连接交易所进行自动交易
- 📊 **可视化** - Web 界面查看交易结果
- 🔧 **策略开发** - Python 编写自定义交易策略
- 📉 **风险管理** - 内置风险控制和资金管理
- 🔄 **多交易所** - 支持多个主流加密货币交易所

## 系统要求

- **Python** >= 3.10 and <= 3.13
- **pip** >= 23
- **PostgreSQL** >= 10
- **Redis** >= 5

## 支持的交易所

### 现货交易
- Binance / Binance US
- Bybit

### 期货/永续合约
- Binance Futures
- Bybit USDT/USDC Perpetual
- Bitget USDT Perpetual
- DYDX Perpetual

## 快速开始

1. **环境准备**: 安装 Python、PostgreSQL 和 Redis
2. **创建项目**: 克隆项目模板
3. **配置环境**: 编辑 `.env` 文件
4. **安装 Jesse**: `pip install jesse`
5. **启动服务**: `jesse run`
6. **访问界面**: 打开 http://localhost:9000

## 文档使用指南

### 新手入门
如果你是 Jesse 新手，建议按以下顺序阅读：
1. [快速开始指南](getting-started.md)
2. [环境配置](environment-setup.md) 或 [Docker 部署](docker.md)
3. [配置说明](configuration.md)
4. [策略开发](strategies.md)
5. [回测分析](backtest.md)

### 开发者指南
对于有经验的开发者：
1. [Docker 部署](docker.md) - 快速搭建环境
2. [策略开发](strategies.md) - 核心开发内容
3. [工具函数](utils.md) - API 参考
4. [调试技巧](debugging.md) - 问题排查

### 运维指南
对于生产环境部署：
1. [环境配置](environment-setup.md) - 生产环境设置
2. [配置说明](configuration.md) - 安全配置
3. [更新升级](update.md) - 版本管理
4. [实盘交易](live-trading.md) - 实盘部署

## 社区和支持

### 官方资源
- [官方网站](https://jesse.trade/)
- [官方文档](https://docs.jesse.trade/)
- [GitHub 仓库](https://github.com/jesse-ai/jesse)
- [PyPI 包](https://pypi.org/project/jesse/)

### 社区资源
- [Discord 社区](https://jesse.trade/discord) - 实时讨论和支持
- [Telegram 群组](https://t.me/jesse_trade) - 社区交流
- [视频教程](https://jesse.trade/youtube) - 官方教学视频
- [策略市场](https://jesse.trade/strategies) - 策略分享平台

### 学习资源
- [JesseGPT](https://jesse.trade/gpt) - AI 助手
- [博客文章](https://jesse.trade/blog) - 技术文章和教程
- [帮助中心](https://jesse.trade/help) - 常见问题解答
- [社区资源](https://github.com/jesse-ai/awesome-jesse/) - 第三方工具和资源

## 注意事项

⚠️ **风险警告**：
- 算法交易存在风险，可能导致资金损失
- 回测结果不保证未来收益
- 请在充分了解风险的情况下使用
- 建议先在测试环境中验证策略

📝 **免责声明**：
- 我们不保证任何交易结果的盈利性
- 请自行承担使用本软件的风险
- 作者和所有关联方不承担任何交易结果的责任
- 不要投入你无法承受损失的资金

## 贡献

欢迎为 Jesse 文档做出贡献：
- 报告文档错误或不准确之处
- 提出改进建议
- 翻译文档到其他语言
- 分享使用经验和最佳实践

## 许可证

Jesse 遵循其原始许可证条款。请查看 [LICENSE](../LICENSE) 文件了解详情。
