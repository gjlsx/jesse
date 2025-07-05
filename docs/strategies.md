# 策略开发

Jesse 提供了强大的 API 来定义自定义交易策略。无论预制策略是否适合你的目的，Jesse 的策略定义 API 才是它真正闪光的地方。

🎥 **视频教程**：如果你更喜欢观看视频，这里有一个 [简短的录屏，逐步解释下面的流程图](https://youtu.be/e0iMTbwFbs4)。

## 策略执行流程

Jesse 等待接收新的蜡烛图数据。当收到时，它会通过一系列函数来做决策。以下是展示步骤的流程图：

![Jesse 策略流程图](https://docs.jesse.trade/assets/jesse-strategy-flowchart.CtbqxXPb.svg)

还有[事件](events.md)的概念，这些是你用来确定在特定事件发生后应该做什么的函数。这些可能在任何时候发生，不一定在蜡烛图关闭时。例如，当你的入场订单被执行并且你开仓新头寸时，会调用 `on_open_position` 事件。

## 策略文件结构

每个策略都是一个继承自 Jesse 基础策略类的 Python 类。基本结构如下：

```python
from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class YourStrategy(Strategy):
    def should_long(self) -> bool:
        """
        决定是否应该开多头仓位
        """
        return False
    
    def should_short(self) -> bool:
        """
        决定是否应该开空头仓位
        """
        return False
    
    def should_cancel_entry(self) -> bool:
        """
        决定是否应该取消入场订单
        """
        return False
    
    def go_long(self):
        """
        执行开多头仓位的逻辑
        """
        qty = utils.size_to_qty(self.balance * 0.5, self.price)
        self.buy = qty, self.price
    
    def go_short(self):
        """
        执行开空头仓位的逻辑
        """
        qty = utils.size_to_qty(self.balance * 0.5, self.price)
        self.sell = qty, self.price
    
    def update_position(self):
        """
        更新现有仓位（可选）
        """
        pass
```

## 核心方法说明

### 1. should_long() 和 should_short()
这些方法返回布尔值，决定是否应该开仓：
- `should_long()`: 返回 True 时开多头仓位
- `should_short()`: 返回 True 时开空头仓位

### 2. go_long() 和 go_short()
当决定开仓时执行的具体逻辑：
- 设置仓位大小
- 设置入场价格
- 设置止损和止盈

### 3. should_cancel_entry()
决定是否取消待执行的入场订单

### 4. update_position()
在每个蜡烛图上更新现有仓位的逻辑

## 策略示例

### 简单移动平均策略

```python
from jesse.strategies import Strategy
import jesse.indicators as ta

class MovingAverageCrossover(Strategy):
    @property
    def fast_sma(self):
        return ta.sma(self.candles, period=10, sequential=True)
    
    @property
    def slow_sma(self):
        return ta.sma(self.candles, period=20, sequential=True)
    
    def should_long(self) -> bool:
        # 快线上穿慢线时做多
        return utils.crossed(self.fast_sma, self.slow_sma, direction='above')
    
    def should_short(self) -> bool:
        # 快线下穿慢线时做空
        return utils.crossed(self.fast_sma, self.slow_sma, direction='below')
    
    def go_long(self):
        # 使用50%的余额开多
        qty = utils.size_to_qty(self.balance * 0.5, self.price)
        self.buy = qty, self.price
        # 设置止损在慢均线下方1%
        self.stop_loss = qty, self.slow_sma[-1] * 0.99
        # 设置止盈在当前价格上方2%
        self.take_profit = qty, self.price * 1.02
    
    def go_short(self):
        # 使用50%的余额开空
        qty = utils.size_to_qty(self.balance * 0.5, self.price)
        self.sell = qty, self.price
        # 设置止损在慢均线上方1%
        self.stop_loss = qty, self.slow_sma[-1] * 1.01
        # 设置止盈在当前价格下方2%
        self.take_profit = qty, self.price * 0.98
```

### RSI 均值回归策略

```python
from jesse.strategies import Strategy
import jesse.indicators as ta

class RSIMeanReversion(Strategy):
    def __init__(self):
        super().__init__()
        self.rsi_period = 14
        self.oversold_threshold = 30
        self.overbought_threshold = 70
    
    @property
    def rsi(self):
        return ta.rsi(self.candles, period=self.rsi_period)
    
    def should_long(self) -> bool:
        # RSI 超卖时做多
        return self.rsi <= self.oversold_threshold
    
    def should_short(self) -> bool:
        # RSI 超买时做空
        return self.rsi >= self.overbought_threshold
    
    def should_cancel_entry(self) -> bool:
        # 如果RSI回到中性区域，取消入场订单
        return 40 < self.rsi < 60
    
    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.3, self.price)
        self.buy = qty, self.price
    
    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.3, self.price)
        self.sell = qty, self.price
    
    def update_position(self):
        # 如果持有多头且RSI超买，平仓
        if self.is_long and self.rsi >= self.overbought_threshold:
            self.liquidate()
        # 如果持有空头且RSI超卖，平仓
        elif self.is_short and self.rsi <= self.oversold_threshold:
            self.liquidate()
```

## 可用属性和方法

### 价格数据
- `self.candles`: 历史蜡烛图数据
- `self.price`: 当前价格
- `self.open`: 当前蜡烛图开盘价
- `self.high`: 当前蜡烛图最高价
- `self.low`: 当前蜡烛图最低价
- `self.close`: 当前蜡烛图收盘价
- `self.volume`: 当前蜡烛图成交量

### 仓位信息
- `self.position`: 当前仓位对象
- `self.is_long`: 是否持有多头仓位
- `self.is_short`: 是否持有空头仓位
- `self.position.qty`: 仓位数量
- `self.position.entry_price`: 入场价格
- `self.position.pnl`: 未实现盈亏
- `self.position.pnl_percentage`: 未实现盈亏百分比

### 账户信息
- `self.balance`: 账户余额
- `self.available_margin`: 可用保证金
- `self.leverage`: 杠杆倍数

### 订单操作
- `self.buy`: 买入订单
- `self.sell`: 卖出订单
- `self.stop_loss`: 止损订单
- `self.take_profit`: 止盈订单
- `self.liquidate()`: 平仓

## 技术指标

Jesse 提供了丰富的技术指标库：

### 趋势指标
- `ta.sma()`: 简单移动平均
- `ta.ema()`: 指数移动平均
- `ta.wma()`: 加权移动平均
- `ta.macd()`: MACD
- `ta.adx()`: 平均方向指数

### 震荡指标
- `ta.rsi()`: 相对强弱指数
- `ta.stoch()`: 随机指标
- `ta.cci()`: 商品通道指数
- `ta.williams_r()`: 威廉指标

### 成交量指标
- `ta.ad()`: 累积/派发线
- `ta.adl()`: 累积/派发线
- `ta.obv()`: 能量潮

### 支撑阻力
- `ta.support_resistance()`: 支撑阻力位
- `ta.pivot_points()`: 枢轴点

## 过滤器 (Filters)

过滤器用于在策略信号触发前添加额外的条件检查：

```python
def filters(self):
    return [
        self.filter_trend(),
        self.filter_volatility(),
        self.filter_volume()
    ]

def filter_trend(self):
    # 只在上升趋势中做多
    ema_50 = ta.ema(self.candles, 50)
    ema_200 = ta.ema(self.candles, 200)
    return ema_50 > ema_200

def filter_volatility(self):
    # 只在低波动时交易
    atr = ta.atr(self.candles, 14)
    return atr < self.price * 0.02  # ATR小于价格的2%

def filter_volume(self):
    # 只在成交量足够时交易
    avg_volume = ta.sma(self.candles[:, 5], 20)  # 20期平均成交量
    return self.volume > avg_volume * 1.5
```

## 事件处理

策略可以响应各种事件：

```python
def on_open_position(self, order):
    """开仓时触发"""
    self.log(f"开仓: {order.side} {order.qty} @ {order.price}")

def on_close_position(self, order):
    """平仓时触发"""
    self.log(f"平仓: PnL = {self.position.pnl}")

def on_increased_position(self, order):
    """加仓时触发"""
    self.log(f"加仓: {order.qty}")

def on_reduced_position(self, order):
    """减仓时触发"""
    self.log(f"减仓: {order.qty}")

def on_stop_loss(self, order):
    """止损触发时"""
    self.log("止损触发")

def on_take_profit(self, order):
    """止盈触发时"""
    self.log("止盈触发")
```

## 最佳实践

### 1. 风险管理
- 始终设置止损
- 不要冒险超过账户的2-5%
- 使用合理的仓位大小

### 2. 代码组织
- 将复杂逻辑分解为小方法
- 使用有意义的变量名
- 添加注释说明策略逻辑

### 3. 测试和优化
- 在多个时间段测试策略
- 使用不同的市场条件
- 避免过度拟合

### 4. 性能考虑
- 缓存计算结果
- 避免在每个蜡烛图上重复计算
- 使用 `sequential=True` 获取历史数据

### 5. 调试技巧
- 使用 `self.log()` 记录重要信息
- 保存中间计算结果
- 使用图表可视化策略表现

## 下一步

- [生成新策略](generating-new-strategy.md)
- [入场和出场](entering-and-exiting.md)
- [事件处理](events.md)
- [过滤器使用](filters.md)
- [API 参考](api.md)
