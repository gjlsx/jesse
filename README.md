<div align="center">
<br>
<p align="center">
<img src="assets/jesse-logo.png" alt="Jesse" height="72" />
</p>

<p align="center">
算法交易曾经很 😵‍💫，我们让它变得 🤩
</p>
</div>

# Jesse
[![PyPI](https://img.shields.io/pypi/v/jesse)](https://pypi.org/project/jesse)
[![Downloads](https://pepy.tech/badge/jesse)](https://pepy.tech/project/jesse)
[![Docker Pulls](https://img.shields.io/docker/pulls/salehmir/jesse)](https://hub.docker.com/r/salehmir/jesse)
[![GitHub](https://img.shields.io/github/license/jesse-ai/jesse)](https://github.com/jesse-ai/jesse)
[![coverage](https://codecov.io/gh/jesse-ai/jesse/graph/badge.svg)](https://codecov.io/gh/jesse-ai/jesse)

---

Jesse 是一个先进的加密货币交易框架，旨在**简化**您**研究**和定义**自己的交易策略**，用于回测、优化和实时交易。

## 什么是 Jesse？
观看此视频快速了解 Jesse：

[![Jesse Overview](https://img.youtube.com/vi/0EqN3OOqeJM/0.jpg)](https://www.youtube.com/watch?v=0EqN3OOqeJM)

## 为什么选择 Jesse？
简而言之，Jesse 比其他解决方案更**准确**，也更**简单**。
事实上，它如此简单，如果您已经了解 Python，您可以在**几分钟内**开始使用，而不是**几周或几个月**。

## 核心特性

- 📝 **简洁语法**：用最简单的语法在最短时间内定义简单和高级交易策略。
- 📊 **全面指标库**：访问完整的技术指标库，语法易于使用。
- 📈 **智能下单**：支持市价单、限价单和止损单，自动为您选择最佳订单类型。
- ⏰ **多时间框架和交易对**：同时回测和实时交易多个时间框架和交易对，无前瞻偏差。
- 🔒 **自托管和隐私优先**：考虑到您的隐私，完全自托管以确保您的交易策略和数据保持安全。
- 🛡️ **风险管理**：内置风险管理辅助函数。
- 📋 **指标系统**：全面的指标系统来评估您的交易策略性能。
- 🔍 **调试模式**：通过详细的调试模式观察您的策略运行情况。
- 🔧 **优化模式**：使用 AI 微调您的策略，无需技术背景。
- 📈 **杠杆和做空**：对杠杆交易和做空的一流支持。
- 🔀 **部分成交**：支持通过多个订单进入和退出仓位，提供更大的灵活性。
- 🔔 **高级警报**：在您的策略中创建实时警报以进行有效监控。
- 🤖 **JesseGPT**：Jesse 拥有自己的 GPT，JesseGPT，可以帮助您编写策略、优化策略、调试策略等等。
- 🔧 **内置代码编辑器**：使用内置代码编辑器编写、编辑和调试您的策略。
- 📺 **YouTube 频道**：Jesse 有一个 YouTube 频道，提供逐步讲解示例策略的屏幕录制教程。

## 深入了解 Jesse 的功能

### 极其简单
用极其简单的 Python 编写复杂的交易策略。访问 300+ 指标、多交易对/时间框架支持、现货/期货交易、部分成交和风险管理工具。专注于逻辑，而非样板代码。

```python
class GoldenCross(Strategy):
    def should_long(self):
        # 当 EMA 8 高于 EMA 21 时做多
        short_ema = ta.ema(self.candles, 8)
        long_ema = ta.ema(self.candles, 21)
        return short_ema > long_ema

    def go_long(self):
        entry_price = self.price - 10        # 限价买单，低于当前价格 $10
        qty = utils.size_to_qty(self.balance*0.05, entry_price) # 只使用总资金的 5%
        self.buy = qty, entry_price                 # 提交入场订单
        self.take_profit = qty, entry_price*1.2  # 止盈价格为入场价格的 120%
        self.stop_loss = qty, entry_price*0.9   # 止损价格为入场价格的 90%
```

### 回测
执行高精度和快速的回测，无前瞻偏差。利用调试日志、支持指标的交互式图表和详细的性能指标来全面验证您的策略。

![Backtest](https://raw.githubusercontent.com/jesse-ai/storage/refs/heads/master/backtest.gif)

### 实时/纸面交易
使用强大的监控工具部署实时策略。支持纸面交易、多账户、实时日志和通知（Telegram、Slack、Discord）、交互式图表、现货/期货、DEX 和内置代码编辑器。

![Live/Paper Trading](https://raw.githubusercontent.com/jesse-ai/storage/refs/heads/master/live.gif)

### 基准测试
使用基准测试功能加速研究。运行批量回测，跨时间框架、交易对和策略进行比较。按关键性能指标过滤和排序结果以进行高效分析。

![Benchmark](https://raw.githubusercontent.com/jesse-ai/storage/refs/heads/master/benchmark.gif)

### AI
即使 Python 知识有限，也可以利用我们的 AI 助手。获得编写和改进策略、实现想法、调试、优化和理解代码的帮助。您的个人 AI 量化分析师。

![AI](https://raw.githubusercontent.com/jesse-ai/storage/refs/heads/master/gpt.gif)

### 优化您的策略
不确定最佳参数？让优化模式使用简单语法来决定。使用 Optuna 库和简单的交叉验证微调任何策略参数。

```python
@property
def slow_sma(self):
    return ta.sma(self.candles, self.hp['slow_sma_period'])

@property
def fast_sma(self):
    return ta.sma(self.candles, self.hp['fast_sma_period'])

def hyperparameters(self):
    return [
        {'name': 'slow_sma_period', 'type': int, 'min': 150, 'max': 210, 'default': 200},
        {'name': 'fast_sma_period', 'type': int, 'min': 20, 'max': 100, 'default': 50},
    ]
```

## 开始使用

### 🚀 快速启动（开发模式）

如果您有Jesse源码并想进行开发调试，可以直接运行而无需安装：

#### 1. 准备工作环境
确保您有一个Jesse项目目录（包含`strategies`和`storage`文件夹）：
```bash
# 如果没有项目目录，创建一个
mkdir my-jesse-project
cd my-jesse-project
mkdir strategies storage
```

#### 2. 配置环境
复制并修改环境配置文件：
```bash
# 复制配置文件
cp path/to/jesse/.env.example .env

# 修改配置为本地运行
POSTGRES_HOST=localhost
REDIS_HOST=localhost
REDIS_PASSWORD=your_password
```

#### 3. 启动Jesse（开发模式）
在您的Jesse项目目录中运行：
```bash
python -c "import sys; sys.path.insert(0, '../jesse'); import jesse; jesse.cli()" run
```

**命令解析**：
- `sys.path.insert(0, '../jesse')` - 添加Jesse源码路径到Python搜索路径
- `import jesse; jesse.cli()` - 导入并启动Jesse命令行接口
- `run` - 执行启动命令

#### 4. 访问Web界面
启动成功后，在浏览器中访问：
```
http://localhost:9000
```

### 📝 **开发模式优势**
- ✅ **无需安装**：直接使用源码运行
- ✅ **实时调试**：修改源码立即生效
- ✅ **路径灵活**：可以在任何Jesse项目目录运行
- ✅ **开发友好**：便于调试和定制功能

### 📚 **标准安装方式**
如果您不需要修改源码，建议使用标准安装：
```bash
pip install jesse
jesse run
```

更多详细信息请参考[官方文档](https://docs.jesse.trade/docs/getting-started)。

## 资源

- [⚡️ 官网](https://jesse.trade)
- [🎓 文档](https://docs.jesse.trade)
- [🎥 YouTube 频道（屏幕录制教程）](https://jesse.trade/youtube)
- [🛟 帮助中心](https://jesse.trade/help)
- [💬 Discord 社区](https://jesse.trade/discord)
- [🤖 JesseGPT](https://jesse.trade/gpt)（需要免费账户）

## 下一步是什么？

您可以在[这里查看项目路线图](https://docs.jesse.trade/docs/roadmap.html)。**订阅**我们在 [jesse.trade](https://jesse.trade) 的邮件列表，以便在好东西发布时第一时间获得。别担心，我们不会发送垃圾邮件——小指起誓。

jesse/
├── __init__.py          # 主入口，包含CLI和Web API
├── config.py           # 核心配置管理
├── strategies/         # 策略模块（包含大量测试策略）
├── controllers/        # 控制器层
├── exchanges/          # 交易所接口
├── indicators/         # 技术指标库
├── models/            # 数据模型
├── services/          # 核心服务
├── modes/             # 不同运行模式（回测、实时等）
└── utils.py           # 工具函数

主要功能
策略开发
简单的Python语法定义交易策略
模块化设计
300+技术指标库
多时间框架和多交易对支持
回测系统
高精度无前瞻偏差的回测
详细的性能指标
交互式图表支持
实时交易
支持现货和期货交易
多交易所支持
实时监控和通知
优化功能
基于Optuna的参数优化
AI辅助策略开发
交叉验证支持
风险管理
内置风险管理工具
止损止盈支持
仓位管理

## 🚀 系统运行流程

### 启动流程
Jesse采用现代化的Web架构，基于uvicorn + FastAPI + GUI的设计：

#### 开发模式启动
```bash
# 在Jesse项目目录中执行
python -c "import sys; sys.path.insert(0, '../jesse'); import jesse; jesse.cli()" run
```

#### 启动步骤
1. **Python路径设置**
   - 将Jesse源码目录添加到Python搜索路径
   - 确保能够导入jesse模块

2. **系统初始化**
   - 显示欢迎信息和版本
   - 验证当前目录是否为Jesse项目
   - 运行数据库迁移
   - 读取环境配置

3. **Web服务启动**
   - 清理旧进程
   - 启动uvicorn异步服务器
   - 注册API路由
   - 挂载静态文件（Nuxt.js前端）

4. **核心组件就绪**
   - 状态存储系统（Store）
   - 进程管理器（ProcessManager）
   - WebSocket实时通信
   - Redis消息中间件

### 完整运行流程图

```
Jesse启动
    ↓
显示欢迎信息
    ↓
验证工作目录
    ↓
运行数据库迁移
    ↓
读取环境配置
    ↓
清理旧进程
    ↓
启动uvicorn服务器
    ↓
注册API路由
    ↓
挂载静态文件
    ↓
等待用户请求
    ↓
┌─────────────────┐
│   请求类型      │
├─────────────────┤
│ 回测 → 创建回测进程
│ 实时交易 → 创建实时交易进程
│ 数据导入 → 创建导入进程
│ 优化 → 创建优化进程
└─────────────────┘
    ↓
策略执行引擎
    ↓
检查过滤器
    ↓
执行交易决策
    ↓
更新仓位和订单
```

## 🧠 策略执行机制

### 核心特点
Jesse的策略执行**不是无限循环线程**，而是采用**事件驱动**和**时间步进**的机制：

### 回测模式：基于历史数据的时间步进
```python
# 有限循环，遍历历史数据
for i in range(0, length, candles_step):
    # 1. 模拟新K线数据
    _simulate_new_candles(candles, i, candles_step)

    # 2. 执行策略路由
    _execute_routes(i, candles_step)

    # 3. 执行市价单
    _execute_market_orders()
```

### 策略执行时机
- **1分钟策略**：每个1分钟K线都执行
- **5分钟策略**：每5个1分钟K线执行一次
- **1小时策略**：每60个1分钟K线执行一次

### 单次策略执行流程
```python
def _execute(self) -> None:
    """策略单次执行入口 - 不是循环！"""
    if self._is_executing:
        return

    self._is_executing = True

    # 执行策略生命周期（一次性）
    self.before()      # 执行前钩子
    self._check()      # 核心检查逻辑
    self.after()       # 执行后钩子

    # 清理并结束
    self._is_executing = False
    self.index += 1    # 移动到下一个时间点
```

### 进程架构
Jesse采用**按任务类型分进程**，而不是按策略分进程：

| 任务类型 | 进程数量 | 策略数量 | 说明 |
|----------|----------|----------|------|
| **回测任务** | 1个进程 | 多个策略 | 所有策略在同一进程中顺序执行 |
| **实时交易** | 1个进程 | 多个策略 | 所有策略共享实时数据流 |
| **优化任务** | 1个进程 | 1个策略 | 优化单个策略的参数 |
| **数据导入** | 1个进程 | 0个策略 | 纯数据处理任务 |

### 实时通信机制
Jesse使用**WebSocket + Redis**实现前后端实时通信：
- WebSocket连接管理器处理客户端连接
- Redis作为消息中间件进行进程间通信
- 实时推送交易状态、日志和性能数据

## 🗃️ 数据库迁移系统

### 什么是数据库迁移？
数据库迁移是一种**版本控制系统**，用于管理数据库结构的变化：

- 📝 **记录数据库结构变化**：每次修改表结构都有记录
- 🔄 **自动更新数据库**：程序启动时自动检查并应用新的结构变化
- 🛡️ **保护现有数据**：在不丢失数据的情况下修改表结构
- 👥 **团队协作**：确保所有开发者的数据库结构一致

### 迁移启动流程
```python
# 在启动Web服务之前，先运行数据库迁移
from jesse.services.migrator import run as run_migrations
try:
    run_migrations()  # 执行迁移
except peewee.OperationalError:
    # 如果数据库还没准备好，等待10秒后重试
    time.sleep(10)
    run_migrations()
```

### 支持的迁移操作
- `ADD` - 添加新字段
- `DROP` - 删除字段
- `RENAME` - 重命名字段
- `MODIFY_TYPE` - 修改字段类型
- `ALLOW_NULL` / `DENY_NULL` - 修改NULL约束
- `ADD_INDEX` / `DROP_INDEX` - 索引管理

### 主要数据表
| 表名 | 用途 | 关键字段 |
|------|------|----------|
| `candle` | K线数据 | exchange, symbol, timeframe, timestamp |
| `order` | 订单记录 | symbol, side, type, qty, price, status |
| `completed_trade` | 完成的交易 | symbol, type, entry_price, exit_price |
| `daily_balance` | 每日余额 | timestamp, balance, available_margin |
| `log` | 系统日志 | timestamp, message, level |

## 🛠️ 开发调试指南

### 源码运行方式详解

Jesse支持直接从源码运行，无需安装包，这对开发和调试非常有用：

#### 命令详解
```bash
python -c "import sys; sys.path.insert(0, '../jesse'); import jesse; jesse.cli()" run
```

**各部分说明**：
1. **`python -c`** - 直接执行Python代码字符串
2. **`import sys`** - 导入系统模块
3. **`sys.path.insert(0, '../jesse')`** - 将Jesse源码目录添加到模块搜索路径最前面
4. **`import jesse`** - 导入Jesse模块
5. **`jesse.cli()`** - 启动Jesse命令行接口
6. **`run`** - 传递给CLI的参数，相当于 `jesse run`

#### 工作原理
```mermaid
graph LR
    A[当前目录: jesseai] --> B[设置Python路径]
    B --> C[导入jesse模块]
    C --> D[启动CLI]
    D --> E[验证项目目录]
    E --> F[启动Web服务]
```

#### 目录结构要求
```
your-workspace/
├── jesse/                 # Jesse源码目录
│   ├── jesse/
│   │   ├── __init__.py
│   │   └── ...
│   └── ...
└── your-project/          # 您的Jesse项目目录
    ├── strategies/        # 策略文件夹
    ├── storage/          # 存储文件夹
    ├── .env             # 环境配置
    └── ...
```

#### 开发调试优势
- **实时修改**：修改Jesse源码后重启即可生效
- **断点调试**：可以在IDE中设置断点调试Jesse内部逻辑
- **自定义功能**：可以添加自定义功能和指标
- **问题排查**：便于定位和解决问题

#### 常见问题解决
1. **ModuleNotFoundError**: 检查路径设置是否正确
2. **工作目录错误**: 确保在包含strategies和storage的目录中运行
3. **数据库连接**: 检查.env文件中的数据库配置


## 免责声明
本软件仅用于教育目的。使用本软件**风险自负**。作者和所有关联方对您的交易结果**不承担任何责任**。**不要冒险投入您害怕失去的资金**。代码中可能存在**错误** - 本软件**不提供任何保证**。
